import logging
# import time
import asyncio
from widgets.clock import Clock
# from datetime import datetime
from screen import Screen

logging.basicConfig(level=logging.DEBUG)

widgets = {
    Clock()
}

async def main():
    with Screen() as s:
        s.add(widgets)
        await s.clear()
        s.widgets["Weather"].add_image("shared/weather_icons/cloudy.png", (200, 200))
        while True:
            for widget in s.widgets.values():
                widget.update()
            # on = time.time()
            await s.refresh_all()
            # method = "refresh_all"
            # off = time.time() - on
            # logging.debug(" %s - Finished in: %.3f s.", method, off)
            await asyncio.sleep(0.2)

if __name__ == "__main__":
    asyncio.run(main())