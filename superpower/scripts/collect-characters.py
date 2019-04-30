import asyncio
from datetime import datetime
import hashlib
import os

import aiohttp
from progress.spinner import Spinner
import requests
import simplejson as json
import uvloop

CHARACTERS_URL = "https://gateway.marvel.com/v1/public/characters"


async def collect_characters(public_key: str, private_key: str):
    """
    Collect all existing characters from the Marvel API
    """
    if not public_key or not private_key:
        print(
            "Please create a Marvel API key and set MARVEL_API_PUBLIC_KEY "
            "and MARVEL_API_PRIVATE_KEY")
        return

    lock = asyncio.Lock()
    characters = []

    params = {
        "limit": 100,
        "apikey": public_key
    }

    spinner = Spinner('Fetching ')
    while True:
        async with aiohttp.ClientSession() as s:
            spinner.next()

            now_string = str(datetime.now().timestamp())
            auth_hash = hashlib.md5()
            auth_hash.update(now_string.encode('utf-8'))
            auth_hash.update(private_key.encode('utf-8'))
            auth_hash.update(public_key.encode('utf-8'))
        
            params["hash"] = auth_hash.hexdigest()
            params["ts"] = now_string

            async with s.get(CHARACTERS_URL, params=params) as r:
                if r.status != 200:
                    print(await r.text())
                    return

                data = await r.json()
                data = data["data"]
                async with lock:
                    characters.extend(data["results"])
                offset = data["offset"] + 101
                params["offset"] = offset

                if data["count"] < 100:
                    print(data["count"])
                    break

    with open("./superpower/characters.json", "w") as f:
        f.write(json.dumps(characters))


if __name__ == "__main__":
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        collect_characters(
            os.getenv("MARVEL_API_PUBLIC_KEY"),
            os.getenv("MARVEL_API_PRIVATE_KEY")
        )
    )