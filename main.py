from PIL import ImageFont
from app.screen import Screen, WIDTH, HEIGHT

TESTING = True

TEXT = "THIS IS A TEST"

screen = Screen()

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 64)

bbox = screen.canvas.textbbox((0, 0), TEXT, font=font)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]
text_pos = ((WIDTH - text_width) // 2, (HEIGHT - text_height) // 2)
screen.canvas.text(text_pos, TEXT, font=font, fill=(255, 0, 0))

if TESTING:
    screen.image.save("__preview/output.png") 
else:
    screen.output()
