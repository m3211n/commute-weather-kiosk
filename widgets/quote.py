import time

class QuoteWidget:
    def __init__(self):
        self.quote = "Be water, my friend."
        self.last_updated = 0
        self.update_interval = 60  # seconds

    async def update(self):
        # Simulate fetching a quote
        self.quote = "Stay hungry, stay foolish."

    async def maybe_update(self):
        if time.monotonic() - self.last_updated >= self.update_interval:
            await self.update()
            self.last_updated = time.monotonic()
            return True
        return False

    def get_html(self):
        return f"""
        <div style="position:absolute; top:100px; left:100px; color:cyan; font-size:24px; font-family:sans-serif;">
            {self.quote}
        </div>
        """