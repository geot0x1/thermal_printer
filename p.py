from PIL import Image, ImageDraw, ImageFont

class ThermalPrinterEmulator:
    def __init__(self, width=384, height=200):
        self.width = width
        self.height = height
        self.page = Image.new('1', (width, height), 1)  # 1-bit, 1=white
        self.current_y = 0

    def draw_pixel(self, x, y, color=0):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.page.putpixel((x, y), color)

    def draw_text(self, text, x=0, y=None, font_size=12):
        """Draw text at pixel level using a bitmap font"""
        if y is None:
            y = self.current_y
        draw = ImageDraw.Draw(self.page)
        try:
            font = ImageFont.truetype("Courier_New.ttf", font_size)
        except:
            font = ImageFont.load_default()
        draw.text((x, y), text, font=font, fill=0)
        self.current_y = y + font_size  # move down for next line

    def show(self):
        self.page.show()

    def clear(self):
        self.page.paste(1, [0, 0, self.width, self.height])

# ---------------- Example usage ----------------
printer = ThermalPrinterEmulator(width=384, height=200)

# Print Hello World
printer.draw_text("Hello World!", x=10, y=10, font_size=16)

# Show the page
printer.show()
