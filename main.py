import logging
import asyncio
from widgets import weather, system
from screen import Screen


async def main():
    logging.basicConfig(level=logging.INFO)

    with Screen() as s:
        s.widgets = [
            system.Clock(),
            weather.Weather(),
            system.Info()
        ]
        await s.refresh(only_dirty=False)
        while True:
            # on = time.time()
            await s.refresh()
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
