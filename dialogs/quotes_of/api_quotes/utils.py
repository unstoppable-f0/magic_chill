from urllib.parse import quote


RUS_VOWELS = ("а", "у", "о", "и", "э", "я", "ю", "е", "ё")


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

    # add space bar between name letters and add html-tags
    for name_part_index in range(name_length-1):
        translated_lower_quote[name_part_index] += ' '
    translated_lower_quote.insert(0, '\n\n<b>')
    translated_lower_quote.insert(name_length+1, '</b>')

    # translate into the right preposition depending on the type of the first letter in the theme word
    if translated_lower_quote[name_length+3][0] in RUS_VOWELS:
        translated_lower_quote[name_length+2] = 'об'
    else:
        translated_lower_quote[name_length+2] = 'о'

    # checking the length of the topic and making necessary space adjustments
    after_preposition_len = name_length + 2
    theme_length = len(translated_lower_quote[after_preposition_len:])
    for i in range(theme_length):
        translated_lower_quote[after_preposition_len + i] = ' ' + translated_lower_quote[after_preposition_len + i]

    # adding the final html-tags
    translated_lower_quote.insert(name_length+2, '<i>')
    translated_lower_quote.insert(translated_lower_quote.index(translated_lower_quote[-1])+1, '</i>')

    translated_lower_quote_str = ''.join(translated_lower_quote)

    return '©'.join((translated_quote[0], translated_lower_quote_str))
