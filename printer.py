from PIL import Image, ImageDraw, ImageFont
from enum import Enum


def byte_to_hex_string(byte):
    return hex(byte).zfill(2).replace("0x", "").zfill(2).upper()


class ThermalPrinterEmulator:
    class State(Enum):
        COMMAND = 1
        TEXT = 2
        GRAPHICS = 3

    def __init__(self, width=384, height=1000):
        self.width = width
        self.height = height
        self.page = Image.new('1', (width, height), 1)
        self.current_x = 0
        self.current_y = 0
        self.font_size = 12
        self.font = self._get_font()
        self.state = self.State.TEXT
        self.command_buffer = ""

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

        char_width = draw.textlength(char, font=self.font)

        self.move_cursor(x=self.current_x + char_width)

    def new_line(self):
        """Add a new line based on the current font size."""
        self.current_x = 0
        self.current_y += self.font_size

    def carriage_return(self):
        self.current_x = 0

    def show(self):
        self.page.show()

    def clear(self):
        self.page.paste(1, [0, 0, self.width, self.height])
        self.current_x = 0
        self.current_y = 0

    def print_graphics(self, byte_value):
        """
        Draws a graphic from a single byte integer.
        The byte represents a column of 8 pixels.
        """
        draw = ImageDraw.Draw(self.page)
        
        # Iterate through the 8 bits of the byte
        for bit_index in range(8):
            # Check if the bit is 'on' (1)
            if (byte_value >> bit_index) & 1:
                # Calculate the pixel coordinates
                x_pixel = self.current_x
                # The bits are drawn from the bottom up, so we reverse the y-coordinate.
                y_pixel = self.current_y + (7 - bit_index)
                
                # Draw a black pixel (fill=0 for black in mode '1' image)
                draw.point((x_pixel, y_pixel), fill=0)
        
        # Advance the cursor by one pixel column
        self.current_x += 1

    
    def print(self, byte):
        if byte == 0x1B:
            self.state = self.State.COMMAND
            b = byte_to_hex_string(byte)
            self.command_buffer = ""
            self.command_buffer += b
            return

        if self.state == self.State.COMMAND:
            self.command_buffer += byte_to_hex_string(byte)
            if self.command_buffer == "1B4108":
                print("1B4108 detected")
                self.state = self.State.TEXT
            elif self.command_buffer == "1B4B55":
                print("1B4B55 command detected")
                self.state = self.State.GRAPHICS
            elif self.command_buffer == "1B4B59":
                print("1B4B59 command detected")
                self.state = self.State.GRAPHICS
            elif self.command_buffer == "1B410F":
                print("1B410F command detected")
                self.state = self.State.GRAPHICS
            if len(self.command_buffer) >= 6:
                self.command_buffer = ""
            return
        else:
            self.command_buffer = ""

        if self.state == self.State.GRAPHICS:
            if byte == 10:
                self.state = self.State.TEXT
                self.new_line()
                return
            elif byte == 13:
                self.state = self.State.TEXT
                self.carriage_return()
                return
            else:
                self.print_graphics(byte)
            return

        if byte >= 32 and byte < 127:
            self.draw_char(chr(byte))
            self.state = self.State.TEXT
        elif byte == 10:  # Line feed
            self.new_line()
            self.state = self.State.TEXT
        elif byte == 13:  # Carriage return
            self.carriage_return()
            self.state = self.State.TEXT


if __name__ == '__main__':
    printer = ThermalPrinterEmulator(width=480, height=800)

    # Move cursor to a starting position
    printer.move_cursor(x=10, y=10)

    # Print a solid vertical line (hex FF)
    for _ in range(8):  # print 8 bytes to make a small square
        printer.print_graphics(0xFF)

    # Add some space
    printer.move_cursor(x=20, y=10)
    
    # Print a dotted line (hex 55)
    for _ in range(8):
        printer.print_graphics(0x55)
        
    # Add some space
    printer.move_cursor(x=30, y=10)

    # Print a line with two dots at the bottom (hex 03)
    for _ in range(8):
        printer.print_graphics(0x03)
    
    printer.show()
