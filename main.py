import os
import sys
import pygame
import time
from datetime import datetime

# Tell SDL to use the framebuffer console
os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.putenv('SDL_FBDEV', '/dev/fb0')
os.putenv('SDL_NOMOUSE', '1')  # optional: disable mouse

# Init pygame
pygame.init()

# Set screen resolution
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1200
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)

# Hide the cursor
pygame.mouse.set_visible(False)

# Set up fonts
pygame.font.init()
font_big = pygame.font.Font('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 72)
font_small = pygame.font.Font(None, 36)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)

# Main loop
try:
    while True:
        screen.fill(BLACK)

        # Draw clock
        now = datetime.now().strftime("%H:%M:%S")
        text_surface = font_big.render(now, True, WHITE)
        screen.blit(text_surface, (100, 100))

        # Draw quote
        quote_surface = font_small.render("Be water, my friend.", True, CYAN)
        screen.blit(quote_surface, (100, 200))

        # Flip to framebuffer
        pygame.display.update()

        time.sleep(1)

except KeyboardInterrupt:
    pygame.quit()
    sys.exit()
