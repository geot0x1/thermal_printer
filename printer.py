from PIL import Image

class ThermalPrinterEmulator:
    def __init__(self, width=384, height=1000):
        """
        Initialize the emulator with a blank page.
        width: pixels
        height: pixels (can be tall for long receipts)
        """
        self.width = width
        self.height = height
        self.page = Image.new('1', (width, height), 1)  # '1' = 1-bit pixels, 1=white
        self.current_y = 0  # tracks where to "print next"

    def draw_pixel(self, x, y, color=0):
        """
        Set a single pixel on the page.
        x, y: pixel coordinates
        color: 0=black, 1=white
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            self.page.putpixel((x, y), color)

    def draw_pixels(self, pixel_list):
        """
        Draw multiple pixels at once.
        pixel_list: list of tuples (x, y, color)
        """
        for x, y, color in pixel_list:
            self.draw_pixel(x, y, color)

    def show(self):
        """Display the current page"""
        self.page.show()

    def clear(self):
        """Clear the page"""
        self.page.paste(1, [0, 0, self.width, self.height])

# ---------------- Example usage ----------------
printer = ThermalPrinterEmulator(width=384, height=600)

# Draw a diagonal line
for i in range(100):
    printer.draw_pixel(i, i)

# Draw a small square
for x in range(50, 70):
    for y in range(20, 40):
        printer.draw_pixel(x, y)

# Draw custom pixels
custom = [(x, 60, 0) for x in range(100, 120)]
printer.draw_pixels(custom)

# Show the page
printer.show()
