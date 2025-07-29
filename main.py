import logging
import locale

import asyncio

from widgets import Clock
from screen import Screen

logging.basicConfig(level=logging.INFO)
locale.setlocale(locale.LC_ALL, "sv_SE.UTF-8")


async def main():
    with Screen() as s:
        s.widgets = [
            Clock()
        ]
        await s.refresh_all(dirty_only=False)
        while True:
            # on = time.time()
            response = await s.refresh_all()
            logging.info(" Screen loop reported: %s", response)
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
