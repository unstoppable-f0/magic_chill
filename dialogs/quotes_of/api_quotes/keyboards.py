from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from dialogs.quotes_of.api_quotes.utils import create_google_search_link


def quote_inline_keyboard(translated: bool = False) -> InlineKeyboardMarkup:
    """Construct an inline keyboard for quote-messages"""

    # creating of a builder
    quote_inline_builder = InlineKeyboardBuilder()

    # Collecting keys of our future keyboard
    quote_inline_buttons = [
        InlineKeyboardButton(text="Hit me another 🗞", callback_data="more_quotes"),
        InlineKeyboardButton(text="Who's author? 🤵‍♀️🤵‍♂️", callback_data='who_is_author')
    ]
    if not translated:  # checking if the quote is already translated
        quote_inline_buttons.append(InlineKeyboardButton(text="Перевод на русский 🇷🇺", callback_data='translate'))

    quote_inline_builder.add(*quote_inline_buttons)
    quote_inline_builder.adjust(1)

    return quote_inline_builder.as_markup()


def author_inline_keyboard(author_name: str, wiki_link: str, lang: str) -> InlineKeyboardMarkup:
    """Construct an inline keyboard for message answer about the author of the sent quote"""

    author_inline_builder = InlineKeyboardBuilder()

    if lang == 'en':
        if wiki_link:
            author_inline_builder.add(InlineKeyboardButton(text='Go to Wikipedia', url=f'{wiki_link}'))
        author_inline_builder.add(InlineKeyboardButton(text='Google him/her!',
                                                       url=f'{create_google_search_link(author_name)}'))

    else:
        if wiki_link:
            author_inline_builder.add(InlineKeyboardButton(text='Перейти на википедию', url=f'{wiki_link}'))
        author_inline_builder.add(InlineKeyboardButton(text='Загуглить его/её!',
                                                       url=f'{create_google_search_link(author_name)}'))

    author_inline_builder.adjust(1)

    return author_inline_builder.as_markup()

