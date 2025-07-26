import asyncio
from screen import Screen
from section import Section
from widgets import Widget
from datetime import datetime

async def main():
    section_top = Section(x=0, y=0, width=1920, height=200)
    section_main = Section(x=0, y=200, width=1920, height=880)

    # Create widgets
    clock = Widget(300, 100)
    quote = Widget(800, 100)

    # Fill widgets
    clock.text((10, 10), datetime.now().strftime("%H:%M:%S"), font_size=48)
    quote.text((10, 10), "Be water, my friend.", font_size=24, color="cyan")

    # Add widgets to sections
    section_top.add(50, 50, clock)
    section_main.add(100, 100, quote)

    screen = Screen()

    while True:
        screen.compose([section_top, section_main])
        await screen.output()
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
