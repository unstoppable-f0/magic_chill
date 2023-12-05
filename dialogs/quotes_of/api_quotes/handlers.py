from . import getters
from ..quotes_menu import router
from utils.translator.google_translator import EasyGoogleTranslate

from typing import Optional

import aiohttp
import json
from random import choice

from aiogram import F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def quote_inline_keyboard(translated: bool = False) -> InlineKeyboardMarkup:
    """Construct an inline keyboard for quote-messages"""

    # creating of a builder
    quote_inline_builder = InlineKeyboardBuilder()

    # Collecting keys of our future keyboard
    quote_inline_buttons = [
        InlineKeyboardButton(text="Hit me another 🗞", callback_data="more_quotes"),
        InlineKeyboardButton(text="Who's author? 🤵‍♀️🤵‍♂️", callback_data='who_author')
    ]
    if not translated:  # checking if the quote is already translated
        quote_inline_buttons.append(InlineKeyboardButton(text="Перевод на русский 🇷🇺", callback_data='translate'))

    quote_inline_builder.add(*quote_inline_buttons)
    quote_inline_builder.adjust(1)

    return quote_inline_builder.as_markup()


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
    """Отправляем сообщение с цитатой в ответ на фразу (кнопку)"""

    quote_dict = await get_quote()
    if quote_dict:
        await message.answer(f'"{quote_dict.get("quote")}" ©\n\n'
                             f'<b>{quote_dict.get("author")}</b> on <i>{quote_dict.get("category")}</i>',
                             reply_markup=quote_inline_keyboard())
    else:
        await message.answer("Something gone wrong. Please, try again or contact the developer")


@router.callback_query(F.data == "more_quotes")
async def more_quotes(callback: CallbackQuery) -> None:
    """Отправляем сообщение с цитатой в ответ на нажатие inline-кнопки"""

    quote_dict = await get_quote()
    if quote_dict:
        await callback.message.answer(f'"{quote_dict.get("quote")}" ©\n\n'
                                      f'<b>{quote_dict.get("author")}</b> on <i>{quote_dict.get("category")}</i>',
                                      reply_markup=quote_inline_keyboard())
    else:
        await callback.message.answer("Something gone wrong. Please, try again or contact the developer")


@router.callback_query(F.data == 'translate')
async def translate(callback: CallbackQuery) -> None:
    """Translates the message to russian via parsing google-translate"""

    translator = EasyGoogleTranslate(source_language='en', target_language='ru')
    translated_quote = await translator.translate(callback.message.text)

    await callback.message.edit_text(text=f'{callback.message.text}'
                                          f'\n'
                                          f'{"-"*35}'
                                          f'\n'
                                          f'{translated_quote}',
                                     reply_markup=quote_inline_keyboard(translated=True))


@router.callback_query(F.data == 'who_author')
async def who_author(callback: CallbackQuery) -> None:
    """Searches for author in the internet"""

    print(callback.message.text)
    await callback.message.answer(text='"Будет информация об авторе"')
