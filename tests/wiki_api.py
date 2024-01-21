from typing import Optional

import aiohttp
import asyncio
import json

from pprint import pprint

# async def get_quote() -> Optional[dict]:
#     """Get a quote via async API-request in the json format"""
#
#     async with aiohttp.ClientSession() as session:
#         api_url = f'https://api.api-ninjas.com/v1/quotes?category={category}'
#         async with session.get(api_url, headers={'X-Api-Key': 'Bubba'}) as response:
#             # json part
#             try:
#                 quote_text = await response.text()
#                 quote_data = json.loads(quote_text)
#                 quote_dict = quote_data[0]
#                 return quote_dict
#
#             except IndexError:
#                 return None


async def get_summary(title: str = None) -> Optional[dict]:
    """Getting the summary by the name from the Wikipedia"""

    async with aiohttp.ClientSession() as session:
        params = {'action': 'query',
                  'prop': 'extracts',
                  'titles': title,
                  'explaintext': 1,
                  'exsentences': 10,
                  'format': 'json'}
        wiki_url = f'https://en.wikipedia.org/w/api.php'

        async with session.get(wiki_url, params=params) as response:
            wiki_page = await response.text()
            return json.loads(wiki_page)


async def main():
    result = await get_summary(title='Abraham Lincoln')
    pprint(result['query'])


if __name__ == '__main__':
    asyncio.run(main())
