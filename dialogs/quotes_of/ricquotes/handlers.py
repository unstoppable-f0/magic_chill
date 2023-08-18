from loader import dp
from database.bot_db import RickDB

from dialogs.states import Ricquotes

from aiogram import F
from aiogram.types import Message

from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.input import TextInput


"""This module includes both scenarios - memorizing and remembering of Ricquotes"""

"""MEMORIZING RICQUOTES DIALOG"""


@dp.message(F.text == "Put new ricquote 🧪")
async def memorize_rick(message: Message, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(state=Ricquotes.start_memorizing, mode=StartMode.RESET_STACK)


async def pages_input_success(message: Message, enter: TextInput, dialog_manager: DialogManager, *args) -> None:
    with RickDB() as rick_db:
        rick_db.update_pages(message.text)
    await message.answer("All is well, I rickdated our database")
    await dialog_manager.done()


async def pages_input_failure(message: Message, enter: TextInput, dialog_manager: DialogManager, *args) -> None:
    await message.answer("Something wrong with your message, please, check it")


def pages_input_validation(user_pages: str):
    """Has to raise ValueError in order for type_factory (aiogram-dialog) to work correctly """
    if not all(page.isdigit() for page in user_pages.split()):
        raise ValueError


"""REMEMBERING RICQUOTES SCENARIO"""


@dp.message(F.text == "Rickmember quotes 🔭")
async def remember_rick(message: Message) -> None:
    with RickDB() as rick_db:
        pages = rick_db.get_pages()
    if pages:
        await message.answer(f"Rick remembers everything!\n{pages}")
    else:
        await message.answer("Something went wrong. Either there are no quotes or there has been a programming "
                             "mistake. In this case contact the developer!")

