import time
from PIL import ImageFont

class QuoteWidget:
    def __init__(self):
        self.quote = "Be water, my friend."
        self.last_updated = 0
        self.update_interval = 60
        self.x = 100
        self.y = 100
        self.font = ImageFont.load_default()

    async def update(self):
        self.quote = "Stay hungry, stay foolish."

    async def maybe_update(self):
        if time.monotonic() - self.last_updated >= self.update_interval:
            await self.update()
            self.last_updated = time.monotonic()
            return True
        return False

    def draw(self, draw):
        draw.text((self.x, self.y), self.quote, fill="cyan", font=self.font)