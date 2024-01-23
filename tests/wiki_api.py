from typing import Optional

import aiohttp
import asyncio
import json
from multidict import MultiDict
from pprint import pprint   # TESTING PURPOSES


async def get_summary(title: str = None) -> Optional[dict]:
    """Getting the summary by the name from the Wikipedia"""

    async with aiohttp.ClientSession() as session:
        params = MultiDict([
            ('action', 'query'),
            ('prop', 'extracts|info|langlinks'),
            ('titles', title),
            ('explaintext', 1),
            ('exsentences', 5),
            ('inprop', 'url'),
            ('lllang', 'ru'),
            ('llprop', 'url'),
            ('format', 'json'),
        ])
        wiki_url = f'https://en.wikipedia.org/w/api.php'

        async with session.get(wiki_url, params=params) as response:
            wiki_page = await response.text()
            return json.loads(wiki_page)


async def main():
    # result = await get_summary(title='Abraham Lincoln')
    result = await get_summary(title='Harry Potter')

    pprint(result)


if __name__ == '__main__':
    asyncio.run(main())
