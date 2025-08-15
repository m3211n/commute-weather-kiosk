import logging
import asyncio
import argparse

from core.screen import Screen
from dashboard import Dashboard


async def main(using_fb=True):
    logging.basicConfig(level=logging.INFO)

    dashboard = Dashboard()
    asyncio.create_task(dashboard.run_forever())

    with Screen(using_fb) as s:
        s.content = dashboard.widgets
        await s.refresh(only_dirty=False)
        while True:
            # on = time.time()
            await s.refresh()
            await asyncio.sleep(5)

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
 