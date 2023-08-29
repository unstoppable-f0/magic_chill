from typing import List

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton


router = Router()

"""All quotes Menu"""
quotes_menu_buttons: List[List] = [
    [
        KeyboardButton(text="Ricquotes 🔬"),
        KeyboardButton(text="Explore human minds 🧠")
    ]
]

quotes_menu_keyboards = ReplyKeyboardMarkup(keyboard=quotes_menu_buttons, resize_keyboard=True, one_time_keyboard=True,
                                            row_width=2)

"""Ricquotes Menu"""
ricquotes_menu_buttons: List[List] = [
    [
        KeyboardButton(text="Put new ricquote 🧪"),
        KeyboardButton(text="Rickmember quotes 🔭")
    ]
]

ricquotes_menu_keyboard = ReplyKeyboardMarkup(keyboard=ricquotes_menu_buttons, resize_keyboard=True,
                                              one_time_keyboard=True,
                                              row_width=2)


@router.message(F.text == "Quotes of 💭")
async def quotes_menu(message: Message) -> None:
    await message.answer("Quotes of great (and not so much) people (and not so much)! 🗯",
                         reply_markup=quotes_menu_keyboards)


@router.message(F.text == "Ricquotes 🔬")
async def ricquotes_menu(message: Message) -> None:
    await message.answer("It's Ricking time!", reply_markup=ricquotes_menu_keyboard)
