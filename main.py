import asyncio
from screen import Screen
from section import Section
from widgets.clock import ClockWidget
from widgets.quote import QuoteWidget

async def main():
    sections = [
        Section(x=0, y=0, width=1920, height=200, widgets=[ClockWidget()]),
        Section(x=0, y=200, width=1920, height=880, widgets=[QuoteWidget()]),
    ]

    screen = Screen()

    while True:
        updated = False

        # Update widgets
        for section in sections:
            for widget in section.widgets:
                if await widget.maybe_update():
                    updated = True

        if updated:
            for s in sections:
                s.render()
            screen_image = screen.compose(sections)
            await screen.output(screen_image)

        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
