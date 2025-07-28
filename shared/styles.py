from PIL import ImageFont

DejaVuSans = lambda size: ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
Mono = lambda size: ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", size) 

class Fonts:
    value = DejaVuSans(80)
    title = Mono(40)
    weather_today = DejaVuSans(120)
    clock = DejaVuSans(240)

class Colors:
    panel_bg = (32, 32, 32)
    title = (88, 88, 88)
    departure_times = (216, 216, 0)
    default = (216, 216, 216)