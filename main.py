import logging
import asyncio
import argparse

from core.screen import Screen
from dashboard import Dashboard


async def main(using_fb=True):
    logging.basicConfig(level=logging.INFO)

    dashboard = Dashboard()

    # Make sure dashboard state is updated before first refresh
    asyncio.create_task(dashboard.run())

    with Screen(using_fb) as s:
        s.content = dashboard.widgets
        while True:
            await s.refresh()
            await asyncio.sleep(0.2)

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
