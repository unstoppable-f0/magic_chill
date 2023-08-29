import requests
import json
from random import choice

from . import getters  # MAYBE TROUBLES WITH THIS IMPORT

from aiogram import F

from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button

from ..quotes_menu import router


@router.message(F.text == "Explore human minds 🧠")
async def get_quote(message: Message):
    category = choice(getters.categories)
    api_url = 'https://api.api-ninjas.com/v1/quotes?category={}'.format(category)
    response = requests.get(api_url, headers={'X-Api-Key': 'GvQEqVdLigY5wM5yLpu4Lw==CgQcF8Xnmu2P9JwM'})
    quote_data = json.loads(response.text)
    try:
        quote_dict: dict = quote_data[0]
        # {'quote': 'Success is 99 percent failure.', 'author': 'Soichiro Honda', 'category': 'failure'}

        await message.answer(f'"{quote_dict.get("quote")}" ©\n\n'
                             f'<b>{quote_dict.get("author")}</b> on <i>{quote_dict.get("category")}</i>')
    except IndexError:
        await message.answer("Something gone wrong. Please, try again or contact the developer")

