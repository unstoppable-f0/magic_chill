from typing import Optional, Tuple
import json
import aiohttp

from multidict import MultiDict
from random import choice


categories = (
    "age",
    "alone",
    "amazing",
    "anger",
    "architecture",
    "art",
    "attitude",
    "beauty",
    "best",
    "birthday",
    "business",
    "car",
    "change",
    "communications",
    "computers",
    "cool",
    "courage",
    "dad",
    "dating",
    "death",
    "design",
    "dreams",
    "education",
    "environmental",
    "equality",
    "experience",
    "failure",
    "faith",
    "family",
    "famous",
    "fear",
    "fitness",
    "food",
    "forgiveness",
    "freedom",
    "friendship",
    "funny",
    "future",
    "god",
    "good",
    "government",
    "graduation",
    "great",
    "happiness",
    "health",
    "history",
    "home",
    "hope",
    "humor",
    "imagination",
    "inspirational",
    "intelligence",
    "jealousy",
    "knowledge",
    "leadership",
    "learning",
    "legal",
    "life",
    "love",
    "marriage",
    "medical",
    "men",
    "mom",
    "money",
    "morning",
    "movies",
    "success",
)


async def get_quote() -> Optional[dict]:
    """Get a quote via async API-request in the json format"""

    async with aiohttp.ClientSession() as session:
        category = choice(categories)
        api_url = f'https://api.api-ninjas.com/v1/quotes?category={category}'
        async with session.get(api_url, headers={'X-Api-Key': 'GvQEqVdLigY5wM5yLpu4Lw==CgQcF8Xnmu2P9JwM'}) as response:
            # json part
            try:
                quote_text = await response.text()
                quote_data = json.loads(quote_text)
                quote_dict = quote_data[0]
                return quote_dict

            except IndexError:
                return None


async def wiki_request(title: str, lang: str) -> Optional[Tuple[str, str]]:
    """Getting the summary by the name from the Wikipedia"""

    async with aiohttp.ClientSession() as session:
        params = MultiDict([
            ('action', 'query'),
            ('prop', 'extracts|info'),
            ('titles', title),
            ('explaintext', 1),
            ('exsentences', 5),
            ('inprop', 'url'),
            ('redirects', 1),
            ('format', 'json'),
        ])
        wiki_url = f'https://{lang}.wikipedia.org/w/api.php'

        async with session.get(wiki_url, params=params) as response:
            wiki_page_json = await response.text()
            wiki_page_dict = json.loads(wiki_page_json)

    try:
        page_id = tuple(wiki_page_dict['query']['pages'].keys())[0]
        summary = wiki_page_dict['query']['pages'][page_id]['extract']
        wiki_link = wiki_page_dict['query']['pages'][page_id]['canonicalurl']

    except KeyError:
        wiki_link = None
        if lang == 'en':
            summary = ("Couldn't find a wiki-page for this author. But you can try google him/her."
                       " Push the button for it!")
        else:
            summary = 'Страничка на Википедии не нашлась. Но можно попробовать загуглить автора. Жми на кнопку!'

    return summary, wiki_link
