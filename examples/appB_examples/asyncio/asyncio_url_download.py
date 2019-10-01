#!/usr/bin/python3.7
# asyncio_url_download.py
# pip install aiohttp aiodns aiofiles
# Example: py asyncio_url_download.py

import asyncio, aiofiles
import aiohttp
from typing import List


async def get_html(session: aiohttp.ClientSession, url: str) -> str:
    print(f"Requesting {url}")
    resp = await session.request('GET', url=url)
    data = await resp.text()
    print(f"Received data for {url}")
    return data


async def main(urls: List[str]) -> None:
    # Asynchronous context manager.  Prefer this rather
    # than using a different session for each GET request
    async with aiohttp.ClientSession() as session:
        # create a task object for each URL
        tasks = [get_html(session, url) for url in urls]

        i = 1
        # Process results of tasks greedily as they complete
        for future in asyncio.as_completed(tasks):
            next_html = await future  # get the next available result

            async with aiofiles.open(f"result{i}.html", "w", encoding="utf-8") as f:
                await f.write(next_html)

            print(f"Wrote result{i}.html")
            i += 1

        # asyncio.gather() will wait for the entire task set to be completed:
        # htmls = await asyncio.gather(*tasks, return_exceptions=True)
        # for html in html:  # all tasks are done, now write all results
        #     async with aiofiles.open(f"result{i}.html", "w", encoding="utf-8") as f:
        #         await f.write(html)


if __name__ == '__main__':
    wiki_urls = [
        "https://en.wikipedia.org/wiki/Mobile_country_code",
        "https://en.wikipedia.org/wiki/List_of_compositions_by_Johann_Sebastian_Bach",
        "https://en.wikipedia.org/wiki/List_of_Xbox_One_games"
    ]
    asyncio.run(main(wiki_urls))
