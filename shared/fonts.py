from PIL import ImageFont


DejaVuSans = lambda size: ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
Mono = lambda size: ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", size) 

class Fonts:
    value_small = DejaVuSans(80)
    title = Mono(40)
    weather_temp_large = DejaVuSans(120)
    clock = DejaVuSans(240)
