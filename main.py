import logging
import asyncio
import argparse
from time import perf_counter

from core.framebuffer import FrameBuffer
from dashboard import Dashboard


async def main(using_fb=True):
    from layout import WIDGETS

    logging.basicConfig(level=logging.INFO)

    dashboard = Dashboard()
    for w in WIDGETS:
        dashboard.add_widget(**w)

    # Make sure dashboard state is updated before first refresh
    asyncio.create_task(dashboard.run())
    if using_fb:
        with FrameBuffer() as fb:
            fb.clear()
            while True:
                elapsed = perf_counter()
                for name, widget in dashboard.get_dirty_widgets():
                    buf = await widget._canvas.asRGB565()
                    xy = widget.xy
                    size = widget.size
                    fb.write_at(buf, xy, size)
                    logging.info("<%s> updated", name)
                elapsed = perf_counter() - elapsed
                logging.info(f"Refresh routine complete in: {elapsed:.3f} s.")
                if elapsed < 1:
                    await asyncio.sleep(1 - elapsed)

    else:
        while True:
            elapsed = perf_counter()
            dashboard.debug()
            elapsed = perf_counter() - elapsed
            logging.info(f"Refresh routine complete in: {elapsed:.3f} s.")
            if elapsed < 1:
                await asyncio.sleep(1 - elapsed)


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
