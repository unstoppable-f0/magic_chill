from . import getters
from ..quotes_menu import router

from typing import Optional

import aiohttp
import json
from random import choice

from aiogram import F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

quote_inline_builder = InlineKeyboardBuilder()
quote_inline_buttons = [
    InlineKeyboardButton(text="Перевод на русский 🇷🇺", callback_data='translate'),
    InlineKeyboardButton(text="Who's author?", callback_data='who_author')
]
quote_inline_builder.row(InlineKeyboardButton(text="Hit me another", callback_data="more_quotes"))
quote_inline_builder.add(*quote_inline_buttons)
quote_inline_builder.adjust(1)


async def get_quote() -> Optional[dict]:
    """Получить цитату по API-сервиса и выдать из неё словарь"""

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
                             reply_markup=quote_inline_builder.as_markup())
    else:
        await message.answer("Something gone wrong. Please, try again or contact the developer")


@router.callback_query(F.data == "more_quotes")
async def more_quotes(callback: CallbackQuery) -> None:
    """Отправляем сообщение с цитатой в ответ на нажатие inline-кнопки"""

    quote_dict = await get_quote()
    if quote_dict:
        await callback.message.answer(f'"{quote_dict.get("quote")}" ©\n\n'
                                      f'<b>{quote_dict.get("author")}</b> on <i>{quote_dict.get("category")}</i>',
                                      reply_markup=quote_inline_builder.as_markup())
    else:
        await callback.message.answer("Something gone wrong. Please, try again or contact the developer")


@router.callback_query(F.data == 'translate')
async def translate(callback: CallbackQuery) -> None:
    """Translates the message to russian via parsing google-translate"""

    await callback.message.edit_text('Будет перевод, когда-нибудь')


@router.callback_query(F.data == 'who_author')
async def who_author(callback: CallbackQuery) -> None:
    """Searches for author in the internet"""

    pass
