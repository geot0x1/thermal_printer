from PIL import Image, ImageDraw, ImageFont

class ThermalPrinterEmulator:
    def __init__(self, width=384, height=1000):
        self.width = width
        self.height = height
        self.page = Image.new('1', (width, height), 1)
        self.current_x = 0
        self.current_y = 0
        self.font_size = 12  # Initialize a default font size state
        self.font = self._get_font()

    def _get_font(self):
        """Helper to get font object based on current font_size."""
        try:
            return ImageFont.truetype("CourierPrime-Regular.ttf", self.font_size)
        except IOError:
            return ImageFont.load_default()

    def set_font_size(self, font_size):
        """Set the font size as a state and update the font object."""
        self.font_size = font_size
        self.font = self._get_font()

    def draw_text(self, text, x=None, y=None):
        if x is None:
            x = self.current_x
        if y is None:
            y = self.current_y
        draw = ImageDraw.Draw(self.page)
        draw.text((x, y), text, font=self.font, fill=0)

    def move_cursor(self, x=None, y=None):
        if x is not None:
            self.current_x = x
        if y is not None:
            self.current_y = y

    def draw_char(self, char, x=None, y=None):
        """Draw a single character and advance the cursor based on its width."""
        if x is None:
            x = self.current_x
        if y is None:
            y = self.current_y

        draw = ImageDraw.Draw(self.page)
        draw.text((x, y), char, font=self.font, fill=0)

        # Measure the width of the character
        char_width = draw.textlength(char, font=self.font)

        # Update the cursor position
        self.move_cursor(x=self.current_x + char_width)

    def new_line(self):
        """Add a new line based on the current font size."""
        self.current_x = 0
        self.current_y += self.font_size  # Use the current font size for line height

    def carriage_return(self):
        self.current_x = 0

    def show(self):
        self.page.show()

    def clear(self):
        self.page.paste(1, [0, 0, self.width, self.height])
        self.current_x = 0
        self.current_y = 0

if __name__ == '__main__':
    printer = ThermalPrinterEmulator(width=480, height=800)

    # Set font size using the new function
    printer.set_font_size(20)

    # Draw text without specifying font size, it uses the state
    text = "Hello World! This is a test."
    printer.move_cursor(y=10)
    printer.draw_text(text)

    # Add a new line, which now automatically uses the current font size for spacing
    printer.new_line()
    printer.new_line()

    # # Demonstrate automatic cursor movement with the new line function
    # for i in "This demonstrates automatic cursor movement.":
    #     printer.draw_char(i)
    
    # # Change the font size and see the effect
    # printer.new_line()
    # printer.set_font_size(14)
    printer.draw_text("This text is smaller.")
    # printer.new_line()
    
    # printer.set_font_size(30)
    # printer.draw_text("And this one is larger!")
    # printer.new_line()

    printer.show()