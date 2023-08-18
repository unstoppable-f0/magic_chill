from dialogs.states import Ricquotes
from dialogs.quotes_of.ricquotes import handlers

from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Button, Column, Group, Select, Multiselect
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import MessageInput, TextInput


"""This module includes both scenarios - memorizing and remembering of Ricquotes"""


input_pages_window = Window(
    Const("Send me viewed pages in one message separated by <b>spaces</b>"),
    TextInput(
        id="pages_text_input",
        type_factory=handlers.pages_input_validation,
        on_success=handlers.pages_input_success,
        on_error=handlers.pages_input_failure
    ),
    state=Ricquotes.start_memorizing
)

ricquotes_windows = [
    input_pages_window
]

ricquotes_dialog = Dialog(*ricquotes_windows)
