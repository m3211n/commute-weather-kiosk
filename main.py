import logging
# import time
import asyncio
from widgets.clock import Clock
# from datetime import datetime
from screen import Screen

logging.basicConfig(level=logging.DEBUG)

widgets = {
    Clock(60)
}

async def main():
    with Screen() as s:
        await s.add(widgets)
        await s.start()
        while True:
            for widget in s.widgets.values():
                await widget.update()
            # on = time.time()
            await s.refresh_all()
            # method = "refresh_all"
            # off = time.time() - on
            # logging.debug(" %s - Finished in: %.3f s.", method, off)
            await asyncio.sleep(0.1)

if __name__ == "__main__":
    asyncio.run(main())