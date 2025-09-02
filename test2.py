# This script generates a custom character in the terminal by
# setting individual "bits" within a single character space.
# It uses Unicode Block Elements to create a composite shape.
#
# The character space is divided into a 2x2 grid, with each
# quadrant corresponding to a specific bit in a 4-bit number.
#
# Bit Map:
#   +---+---+
#   | 1 | 2 |  <-- Quadrant 1 and Quadrant 2
#   +---+---+
#   | 4 | 8 |  <-- Quadrant 4 and Quadrant 8
#   +---+---+
#
# A 4-bit integer (0-15) determines which quadrants are filled.
#
# Example:
# - Input 1 (0b0001): Fills the top-left quadrant (▘)
# - Input 5 (0b0101): Fills the top-left and bottom-left quadrants (▙)
# - Input 10 (0b1010): Fills the top-right and bottom-right quadrants (▟)

import sys

def get_custom_char(bit_value):
    """
    Returns a custom character string based on a 4-bit integer value.
    The integer is used as a bitmask to select different quadrants
    of a single Unicode block character.
    
    :param bit_value: An integer from 0 to 15 (0b0000 to 0b1111).
    :return: The corresponding single-character Unicode string.
    """
    # Dictionary mapping a 4-bit integer to the corresponding Unicode character.
    # The keys represent the combined bit values of the quadrants.
    # These characters are part of the Unicode "Block Elements" range.
    char_map = {
        0: ' ',     # 0000 - All off
        1: '▘',    # 0001 - Top-left
        2: '▝',    # 0010 - Top-right
        3: '▀',    # 0011 - Top-half
        4: '▖',    # 0100 - Bottom-left
        5: '▙',    # 0101 - Left-half
        6: '▜',    # 0110 - Top-right & Bottom-left
        7: '▛',    # 0111 - All but bottom-right
        8: '▗',    # 1000 - Bottom-right
        9: '▚',    # 1001 - Top-left & Bottom-right
        10: '▄',   # 1010 - Bottom-half
        11: '▙',   # 1011 - All but top-left
        12: '▟',   # 1100 - Right-half
        13: '▙',   # 1101 - All but top-right
        14: '▜',   # 1110 - All but bottom-left
        15: '█'    # 1111 - Full block
    }
    
    # Ensure the input is within the valid range
    if not (0 <= bit_value <= 15):
        return " " # Return a space for invalid input
    
    return char_map.get(bit_value, ' ')

for i in range(16):
    print(f"Character for value {i}: {get_custom_char(i)}")