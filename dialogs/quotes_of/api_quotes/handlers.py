from . import getters  # MAYBE TROUBLES WITH THIS IMPORT
from ..quotes_menu import router

import requests
import json
from random import choice

from aiogram import F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

quote_builder = InlineKeyboardBuilder()
quote_builder.row(InlineKeyboardButton(text="Hit me another", callback_data="more_quotes"))


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
                             reply_markup=quote_builder.as_markup())
    else:
        await message.answer("Something gone wrong. Please, try again or contact the developer")


@router.callback_query(F.data == "more_quotes")
async def more_quotes(callback: CallbackQuery) -> None:
    quote_dict = get_quote()
    if quote_dict:
        await callback.message.answer(f'"{quote_dict.get("quote")}" ©\n\n'
                                      f'<b>{quote_dict.get("author")}</b> on <i>{quote_dict.get("category")}</i>',
                                      reply_markup=quote_builder.as_markup())
    else:
        await callback.message.answer("Something gone wrong. Please, try again or contact the developer")
