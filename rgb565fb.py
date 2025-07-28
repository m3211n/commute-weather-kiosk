import numpy as np
import freetype

FT_LOAD_RENDER = 4
FT_LOAD_TARGET_MONO = 16

class CanvasRGB565:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.buffer = np.zeros((height, width), dtype='>u2')

    def clear(self, color):
        self.buffer[:, :] = color

    def draw_rect(self, x, y, w, h, color):
        self.buffer[y:y+h, x:x+w] = color

    def draw_line(self, x0, y0, x1, y1, color):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy

        while True:
            if 0 <= x0 < self.width and 0 <= y0 < self.height:
                self.buffer[y0, x0] = color
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def draw_circle(self, cx, cy, radius, color):
        x = radius
        y = 0
        err = 0

        while x >= y:
            for dx, dy in [(x, y), (y, x), (-y, x), (-x, y),
                           (-x, -y), (-y, -x), (y, -x), (x, -y)]:
                px = cx + dx
                py = cy + dy
                if 0 <= px < self.width and 0 <= py < self.height:
                    self.buffer[py, px] = color
            y += 1
            if err <= 0:
                err += 2 * y + 1
            if err > 0:
                x -= 1
                err -= 2 * x + 1

    def draw_polygon(self, points, color):
        for i in range(len(points)):
            x0, y0 = points[i]
            x1, y1 = points[(i + 1) % len(points)]
            self.draw_line(x0, y0, x1, y1, color)

    def draw_text(self, x, y, text, font_path, pixel_size, color):
        face = freetype.Face(font_path)
        face.set_char_size(pixel_size * 64, 0, 96, 96)
        pen_x = x
        for char in text:
            face.load_char(char, FT_LOAD_RENDER | FT_LOAD_TARGET_MONO)
            bitmap = face.glyph.bitmap
            top = face.glyph.bitmap_top
            left = face.glyph.bitmap_left
            w, h = bitmap.width, bitmap.rows
            pitch = bitmap.pitch
            data = bitmap.buffer

            for row in range(h):
                for col in range(w):
                    byte_index = row * pitch + (col // 8)
                    bit_mask = 0x80 >> (col % 8)
                    if data[byte_index] & bit_mask:
                        px = pen_x + left + col
                        py = y + (top - h) + row
                        if 0 <= px < self.width and 0 <= py < self.height:
                            self.buffer[py, px] = color

            pen_x += face.glyph.advance.x // 64 or bitmap.width

    def to_bytes(self):
        return self.buffer.tobytes()

    def blit_to_fb(self, x=0, y=0, fb_path='/dev/fb0', screen_width=1920):
        with open(fb_path, 'r+b') as fb:
            for row in range(self.height):
                offset = ((y + row) * screen_width + x) * 2
                fb.seek(offset)
                fb.write(self.buffer[row].tobytes())
