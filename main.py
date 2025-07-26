import asyncio
from label import Label
from datetime import datetime

label = Label(x=560, y=500, width=800, height=200, font_size=120)

async def main():
    while True:
        now = datetime.now().strftime("%H:%M:%S")
        await label.update(now)
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())