import logging
# import time
import asyncio
from widgets import Clock
# from datetime import datetime
from screen import Screen

logging.basicConfig(level=logging.INFO)

widgets = {
    Clock(60)
}

async def main():
    with Screen() as s:
        await s.add(widgets)
        await s.start()
        while True:
            # on = time.time()
            response = await s.refresh_all()
            logging.info(" Screen loop reported: %s", response)
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())