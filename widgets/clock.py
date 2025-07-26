from datetime import datetime
import time

class ClockWidget:
    def __init__(self):
        self.content = "--:--"
        self.last_updated = 0
        self.update_interval = 1  # seconds

    async def update(self):
        now = datetime.now().strftime("%H:%M:%S")
        self.content = now

    async def maybe_update(self):
        if time.monotonic() - self.last_updated >= self.update_interval:
            await self.update()
            self.last_updated = time.monotonic()
            return True
        return False

    def get_html(self):
        return f"""
        <div style="position:absolute; top:50px; left:50px; color:white; font-size:48px; font-family:sans-serif;">
            {self.content}
        </div>
        """