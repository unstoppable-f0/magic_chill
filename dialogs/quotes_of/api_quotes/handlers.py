from typing import Optional

import aiohttp
import json
from random import choice

from aiogram import F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


from dialogs.quotes_of.api_quotes import getters
from dialogs.quotes_of.api_quotes.utils import create_google_search_link, translate_formatter, wiki_request
from dialogs.quotes_of.quotes_menu import router

from utils.translator.google_translator import EasyGoogleTranslate


def quote_inline_keyboard(translated: bool = False) -> InlineKeyboardMarkup:
    """Construct an inline keyboard for quote-messages"""

    # creating of a builder
    quote_inline_builder = InlineKeyboardBuilder()

    # Collecting keys of our future keyboard
    quote_inline_buttons = [
        InlineKeyboardButton(text="Hit me another 🗞", callback_data="more_quotes"),
        InlineKeyboardButton(text="Who's author? 🤵‍♀️🤵‍♂️", callback_data='who_is_author')
    ]
    if not translated:  # checking if the quote is already translated
        quote_inline_buttons.append(InlineKeyboardButton(text="Перевод на русский 🇷🇺", callback_data='translate'))

    quote_inline_builder.add(*quote_inline_buttons)
    quote_inline_builder.adjust(1)

    return quote_inline_builder.as_markup()


def author_inline_keyboard(author_name: str, wiki_link: str) -> InlineKeyboardMarkup:
    """Construct an inline keyboard for message answer about the author of the sent quote"""

    author_inline_builder = InlineKeyboardBuilder()

    author_inline_buttons = [
        InlineKeyboardButton(text='Перейти на википедию', url=f'{wiki_link}'),
        InlineKeyboardButton(text='Google him/her!', url=f'{create_google_search_link(author_name)}')
    ]

    author_inline_builder.add(*author_inline_buttons)
    author_inline_builder.adjust(1)

    return author_inline_builder.as_markup()


async def get_quote() -> Optional[dict]:
    """Get a quote via async API-request in the json format"""

    async with aiohttp.ClientSession() as session:
        category = choice(getters.categories)
        api_url = f'https://api.api-ninjas.com/v1/quotes?category={category}'
        async with session.get(api_url, headers={'X-Api-Key': 'GvQEqVdLigY5wM5yLpu4Lw==CgQcF8Xnmu2P9JwM'}) as response:
            # json part
            try:
                quote_text = await response.text()
                quote_data = json.loads(quote_text)
                quote_dict = quote_data[0]
                return quote_dict

            except IndexError:
                return None


@router.message(F.text == "Explore human minds 🧠")
async def send_quote(message: Message):
    """Sending a message as answer to the text"""

    quote_dict = await get_quote()
    if quote_dict:
        await message.answer(f'"{quote_dict.get("quote")}" ©\n\n'
                             f'<b>{quote_dict.get("author")}</b> on <i>{quote_dict.get("category")}</i>',
                             reply_markup=quote_inline_keyboard())
    else:
        await message.answer("Something gone wrong. Please, try again or contact the developer")


@router.callback_query(F.data == "more_quotes")
async def more_quotes(callback: CallbackQuery) -> None:
    """Sending a message as answer to the pushing of inline-button"""

    quote_dict = await get_quote()
    if quote_dict:
        await callback.message.answer(f'"{quote_dict.get("quote")}" ©\n\n'
                                      f'<b>{quote_dict.get("author")}</b> on <i>{quote_dict.get("category")}</i>',
                                      reply_markup=quote_inline_keyboard())
    else:
        await callback.message.answer("Something gone wrong. Please, try again or contact the developer")


@router.callback_query(F.data == 'translate')
async def translate(callback: CallbackQuery) -> None:
    """
    Translates the message to russian via parsing google-translate
    Formatting the message using message entities and function 'translate_formatter()' from .utils.py
    """

    translator = EasyGoogleTranslate(source_language='en', target_language='ru')
    translated_quote = await translator.translate(callback.message.text)

    entities = callback.message.entities
    author_entity = entities[0].extract_from(callback.message.text)
    formatted_translated_quote = translate_formatter(translated_quote=translated_quote, author_entity=author_entity)

    await callback.message.edit_text(text=f'{callback.message.html_text}'
                                          f'\n'
                                          f'{"-"*35}'
                                          f'\n'
                                          f'{formatted_translated_quote}',
                                     reply_markup=quote_inline_keyboard(translated=True))


@router.callback_query(F.data == 'who_is_author')
async def who_is_author(callback: CallbackQuery) -> None:
    """
    Searches for author in the internet
    Searches in Wikipedia (eng or rus depends on the language) and creates a google-search link
    """

    author_entity_list = []
    entities = callback.message.entities
    for i_entity in entities:
        if i_entity.type == 'bold':
            author_entity_list.append(i_entity.extract_from(callback.message.text))

    if len(author_entity_list) == 2:
        author_name = author_entity_list[1]
        lang = 'ru'
    else:
        author_name = author_entity_list[0]
        lang = 'en'

    summary, wiki_link = await wiki_request(title=author_name, lang=lang)

    await callback.message.answer(text=summary,
                                  reply_markup=author_inline_keyboard(author_name=author_name, wiki_link=wiki_link))
