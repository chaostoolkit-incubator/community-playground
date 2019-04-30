import asyncio
import os
import os.path

import aiohttp
from progress.bar import ChargingBar
import simplejson as json
import slugify
import uvloop

THUMBNAIL_NOT_FOUND = 'http://i.annihil.us/u/prod/marvel/i/mg/b/40/image_not_available'


async def main():
    """
    Collect characters images from Marvel

    Do not store those which do not have any available image.
    """
    images_dir = "./superpower-static/images"
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)

    with open("./superpower/characters.json", "r") as f:
        characters = json.load(f)
        bar = ChargingBar('Fetching ', max=len(characters))

        for c in characters:
            bar.next()
            async with aiohttp.ClientSession() as s:
                thumbnail = c["thumbnail"]
                if thumbnail["path"] == THUMBNAIL_NOT_FOUND:
                    continue

                img = "{}/{}.{}".format(
                    thumbnail["path"], "portrait_uncanny",
                    thumbnail["extension"])
                async with s.get(img) as r:
                    img_path = os.path.join(
                        images_dir, "{}.{}".format(
                            slugify.slugify(c["name"]), thumbnail["extension"]
                        )
                    )
                    with open(img_path, "wb") as i:
                        i.write(await r.read())
        bar.finish()


if __name__ == '__main__':
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())