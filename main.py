import logging
import asyncio
import argparse

from widgets import weather, system, departures
from core.screen import Screen


async def main(using_fb=True):
    logging.basicConfig(level=logging.DEBUG)

    with Screen(using_fb) as s:
        s.widgets = [
            system.Clock(),
            weather.Weather(),
            system.Info(),
            departures.Trains(),
            departures.Busses()
        ]
        await s.refresh(only_dirty=False)
        while True:
            # on = time.time()
            await s.refresh()
            await asyncio.sleep(1)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Zero 2W Kiosk App")
    parser.add_argument(
        "--fb", "--framebuffer", "--prod",
        dest="fb",
        action="store_true",
        help="Run the app in production mode using framebuffer /dev/fb0"
        )
    args = parser.parse_args()

    asyncio.run(main(using_fb=args.fb))
