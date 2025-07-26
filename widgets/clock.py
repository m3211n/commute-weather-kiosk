from datetime import datetime
import time
from PIL import ImageFont

class ClockWidget:
    def __init__(self):
        self.content = "--:--"
        self.last_updated = 0
        self.update_interval = 1
        self.x = 50
        self.y = 50
        self.font = ImageFont.load_default()

    async def update(self):
        self.content = datetime.now().strftime("%H:%M:%S")

    async def maybe_update(self):
        if time.monotonic() - self.last_updated >= self.update_interval:
            await self.update()
            self.last_updated = time.monotonic()
            return True
        return False

    def draw(self, draw):
        draw.text((self.x, self.y), self.content, fill="white", font=self.font)