from PIL import Image, ImageDraw, ImageFont

class ThermalPrinterEmulator:
    def __init__(self, width=384, height=1000):
        self.width = width
        self.height = height
        self.page = Image.new('1', (width, height), 1)
        self.current_x = 0
        self.current_y = 0

    def draw_text(self, text, x=None, y=None, font_size=12):
        if x is None:
            x = self.current_x
        if y is None:
            y = self.current_y
        draw = ImageDraw.Draw(self.page)
        try:
            font = ImageFont.truetype("Courier_New.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()
        draw.text((x, y), text, font=font, fill=0)

    def move_cursor(self, x=None, y=None):
        if x is not None:
            self.current_x = x
        if y is not None:
            self.current_y = y

    def draw_char(self, char, x=None, y=None, font_size=12):
        """Draw a single character and advance the cursor based on its width."""
        if x is None:
            x = self.current_x
        if y is None:
            y = self.current_y

        draw = ImageDraw.Draw(self.page)
        try:
            font = ImageFont.truetype("CourierPrime-Regular.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()

        # Draw the character
        draw.text((x, y), char, font=font, fill=0)

        # Measure the width of the character
        char_width = draw.textlength(char, font=font)

        # Update the cursor position
        self.move_cursor(x=self.current_x + char_width)

    def new_line(self, line_height=16):
        self.current_x = 0
        self.current_y += line_height

    def carriage_return(self):
        self.current_x = 0

    def show(self):
        self.page.show()

    def clear(self):
        self.page.paste(1, [0, 0, self.width, self.height])
        self.current_x = 0
        self.current_y = 0

if __name__ == '__main__':
    printer = ThermalPrinterEmulator(width=384, height=600)

    # Use a loop to print characters and have the cursor advance automatically
    text = "Hello World! This is a test."
    printer.move_cursor(y=10)
    printer.draw_text(text, font_size=20)

    printer.new_line(line_height=40)

    # Demonstrate automatic cursor movement
    for i in "This demonstrates automatic cursor movement.":
        printer.draw_char(i, font_size=16)

    printer.show()