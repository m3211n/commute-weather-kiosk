from PIL import Image, ImageDraw, ImageFont  # just to ensure import path
print(__import__("PIL").__version__)  # should print 11.3.0

img = Image.new("RGBA", (400, 200), (20,20,20,255))
d = ImageDraw.Draw(img)
f = ImageFont.load_default()
d.multiline_text((200,100), "Hello\nworld", font=f, fill="white", anchor="mm", align="right", spacing=6)
img.save("ok.png")
