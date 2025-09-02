from printer import ThermalPrinterEmulator
from enum import Enum

def openfile():
    with open("tymponogram.log", "rb") as f:
        return f.read()


if __name__ == '__main__':
    myfile = openfile()
    lines = myfile.split(b'\n')
    lines = [line + b'\n' for line in lines] # Appending the \n

    printer = ThermalPrinterEmulator(width=480, height=800)
    printer.set_font_size(16)
    printer.move_cursor(y=10)

    for line in lines:
        char_counter = 0
        for byte in line:
            printer.print(byte)
        # break
        

    # for byte in myfile:
    #     if byte > 32 and byte < 127:
    #         printer.draw_text(chr(byte), x=10, y=10, font_size=16)

    # Draw a diagonal line
    # for i in range(100):
    #     printer.draw_pixel(i, i)

    # # Draw a small square
    # for x in range(50, 70):
    #     for y in range(20, 40):
    #         printer.draw_pixel(x, y)

    # # Draw custom pixels
    # custom = [(x, 60, 0) for x in range(100, 120)]
    # printer.draw_pixels(custom)

    # # Print Hello World
    # printer.draw_text("Hello World!", x=10, y=10, font_size=16)

    # Show the page
    printer.show()