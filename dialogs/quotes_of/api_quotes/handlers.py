from aiogram import F
from aiogram.types import Message, CallbackQuery

from dialogs.quotes_of.api_quotes.getters import get_quote, wiki_request
from dialogs.quotes_of.api_quotes.utils import translate_formatter
from dialogs.quotes_of.quotes_menu import router

from utils.translator.google_translator import EasyGoogleTranslate
from dialogs.quotes_of.api_quotes.keyboards import quote_inline_keyboard, author_inline_keyboard


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
                                  reply_markup=author_inline_keyboard(author_name=author_name,
                                                                      wiki_link=wiki_link,
                                                                      lang=lang))
