import logging
import asyncio
import argparse

from core.screen import Screen
from dashboard import Dashboard


async def main(using_fb=True):
    logging.basicConfig(level=logging.INFO)

    dashboard = Dashboard()

    # Make sure dashboard state is updated before first refresh
    await dashboard.run_once()
    asyncio.create_task(dashboard.run_forever())

    with Screen(using_fb) as s:
        s.content = dashboard.widgets
        while True:
            # on = time.time()
            was_updated = await s.refresh()
            if was_updated:
                await asyncio.sleep(5)
            else:
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
