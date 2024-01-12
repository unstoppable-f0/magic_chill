from urllib.parse import quote


def create_google_search_link(author_name: str) -> str:
    """Create a Google search link"""
    google_base_link = 'https://www.google.com/search?q={}'
    prepared_author_name = quote(author_name.encode('utf-8'))

    return google_base_link.format(prepared_author_name)


def translate_formatter(translated_quote: str, author_entity: str) -> str:
    """
    Change into a beautiful format the lower piece of the quote in russian language
    :param translated_quote: a part of the quote that was translated to russian language
    :param author_entity: an original (in english) author name that is used to count the length of words in the name
    :return: str: ful quote with the formatted lower part
    """

    translated_quote = translated_quote.split('©')
    name_length = len(author_entity.split())

    # beautifying the lower quote string
    translated_lower_quote = translated_quote[1].split()

    for name_part_index in range(name_length-1):
        translated_lower_quote[name_part_index] += ' '

    translated_lower_quote.insert(0, '\n\n<b>')
    translated_lower_quote.insert(name_length+1, '</b>')
    translated_lower_quote[name_length+2] = ' о '
    translated_lower_quote.insert(name_length+2, '<i>')
    translated_lower_quote.insert(translated_lower_quote.index(translated_lower_quote[-1])+1, '</i>')

    # тема словосочетание тоже может быть несколько слов (прим.: окружающая среда)

    translated_lower_quote_str = ''.join(translated_lower_quote)

    return '©'.join((translated_quote[0], translated_lower_quote_str))
