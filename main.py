import asyncio
from label import Label
from datetime import datetime

label = Label(x=50, y=50, width=200, height=50, font_size=32)

async def main():
    while True:
        now = datetime.now().strftime("%H:%M:%S")
        await label.update(now)
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())