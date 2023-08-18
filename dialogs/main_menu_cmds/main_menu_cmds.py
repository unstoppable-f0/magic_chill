from typing import List

from aiogram import Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from aiogram.filters import Command

from aiogram_dialog import DialogManager
from aiogram_dialog.api.exceptions import NoContextError

router = Router()

"""Keyboard for main menu"""
main_menu_buttons: List[List] = [
    [
        KeyboardButton(text="Memorize an event 🗓️"),
        KeyboardButton(text="Remember events 💭")
    ],
    [
        KeyboardButton(text="Literature 📚"),
        KeyboardButton(text="Quotes of 💭"),
    ],
    [
        KeyboardButton(text="Randomize a song 🎲", web_app=WebAppInfo(
            url="https://mydeartestingground.000webhostapp.com/")),
        KeyboardButton(text="Statistics 📊"),
    ]
]
main_menu_keyboard = ReplyKeyboardMarkup(keyboard=main_menu_buttons, resize_keyboard=True, one_time_keyboard=True,
                                         row_width=2)


@router.message(Command('start', 'menu'))
async def start(message: Message) -> None:
    """Function for the activation of the Chill Bot"""
    await message.answer("Hey, choomba! Wanna some magic chilling?",
                         reply_markup=main_menu_keyboard)


@router.message(Command('stop'))
async def stop(message: Message, dialog_manager: DialogManager) -> None:
    """Stop any scenario"""
    try:
        await dialog_manager.done()
    except NoContextError:
        pass
    await message.answer("Our talk has been stopped. If you want to start again - type /start")



