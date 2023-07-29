from typing import List

from aiogram import Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

from aiogram_dialog import DialogManager


router = Router()

"""Keyboard for main menu"""
main_menu_buttons = [
    [
    KeyboardButton(text="Memorize an event 🗓️"),
    # types.KeyboardButton(text="Randomize a song 🎲"),
    KeyboardButton(text="Remember events 💭"),
    # types.KeyboardButton(text="Statistics 📊")
    ]
]
main_menu_keyboard = ReplyKeyboardMarkup(keyboard=main_menu_buttons, resize_keyboard=True, one_time_keyboard=True, row_width=2)


@router.message(Command('start', 'menu'))
async def start(message: Message) -> None:
    """Function for the activation of the Chill Bot"""
    await message.answer("Hey, choomba! Wanna some magic chilling?",
                         reply_markup=main_menu_keyboard)

