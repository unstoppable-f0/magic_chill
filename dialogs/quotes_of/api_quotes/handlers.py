from . import getters
from ..quotes_menu import router

import requests
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


def get_quote():
    """getting a quote with api"""

    category = choice(getters.categories)
    api_url = 'https://api.api-ninjas.com/v1/quotes?category={}'.format(category)
    response = requests.get(api_url, headers={'X-Api-Key': 'GvQEqVdLigY5wM5yLpu4Lw==CgQcF8Xnmu2P9JwM'})
    quote_data = json.loads(response.text)
    try:
        quote_dict: dict = quote_data[0]
        return quote_dict
    except IndexError:
        return False


@router.message(F.text == "Explore human minds 🧠")
async def send_quote(message: Message):
    quote_dict = get_quote()
    if quote_dict:
        await message.answer(f'"{quote_dict.get("quote")}" ©\n\n'
                             f'<b>{quote_dict.get("author")}</b> on <i>{quote_dict.get("category")}</i>',
                             reply_markup=quote_inline_builder.as_markup())
    else:
        await message.answer("Something gone wrong. Please, try again or contact the developer")


@router.callback_query(F.data == "more_quotes")
async def more_quotes(callback: CallbackQuery) -> None:
    quote_dict = get_quote()
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
