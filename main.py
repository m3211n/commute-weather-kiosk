import asyncio
from screen import Screen
from section import Section
from widget import Widget
from datetime import datetime

async def main():
    screen = Screen()

    while True:
        # Rebuild layout every cycle
        section_top = Section(0, 0, 1920, 200)
        section_main = Section(0, 200, 1920, 1000)

        # Clock widget (dynamic)
        clock = Widget(300, 100)
        clock.clear()
        clock.text((10, 10), datetime.now().strftime("%H:%M:%S"), font_size=48)

        # Quote widget (static)
        quote = Widget(800, 100)
        quote.text((10, 10), "Be water, my friend.", font_size=24, color="cyan")

        # Add widgets to sections
        section_top.add(50, 50, clock)
        section_main.add(100, 100, quote)

        # Compose and output
        screen.compose([section_top, section_main])
        await screen.output()
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
