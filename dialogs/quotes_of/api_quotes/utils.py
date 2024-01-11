from urllib.parse import quote


def create_google_search_link(author_name: str) -> str:
    google_base_link = 'https://www.google.com/search?q={}'
    prepared_author_name = quote(author_name.encode('utf-8'))

    return google_base_link.format(prepared_author_name)


def translate_formatter(translated_quote: list[str], author_entity: str) -> tuple[str, str]:
    name_length = len(author_entity.split())

    cleaned_name: list[str] = translated_quote[1].lstrip('\n').split()
    author_name_translated: str = ' '.join(cleaned_name[:name_length])

    # beautifying the lower quote string
    translated_lower_quote = translated_quote[1].split()
    translated_lower_quote[0] = '\n\n<b>'
    translated_lower_quote.insert(name_length, '</b>')
    translated_lower_quote[name_length+1] = ' о '
    translated_lower_quote.insert(name_length+2, '<i>')
    translated_lower_quote.insert(translated_lower_quote.index(translated_lower_quote[-1])+1, '</i>')

    translated_lower_quote_str = ''.join(translated_lower_quote)

    return author_name_translated, translated_lower_quote_str
