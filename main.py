import asyncio
from label import Label
from datetime import datetime

label = Label(x=560, y=500, font_size=120)

async def main():
    while True:
        await label.text(datetime.now().strftime("%H:%M:%S"))
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())