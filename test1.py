# # single_char_pixel.py

# def bits_to_braille(bits):
#     """
#     Convert an 8-bit pattern to a Braille character.
#     bits: list of 8 integers (0 or 1)
#     Braille dots layout:
#     [0] [3]
#     [1] [4]
#     [2] [5]
#     [6] [7]
#     Returns: single unicode character
#     """
#     if len(bits) != 8:
#         raise ValueError("Bits list must have 8 elements")
#     code = 0x2800
#     mapping = [0,1,2,3,4,5,6,7]
#     for i, bit in enumerate(bits):
#         if bit:
#             code += 1 << mapping[i]
#     return chr(code)

# # Example usage:
# # Define 8-bit pattern for a custom pixel inside one char
# # For example, a diagonal pattern
# pattern = [1,1,1,0,0,0,1,0]

# char = bits_to_braille(pattern)
# print(f"Your custom character: {char}")

bits = [1,0,0,0,0,0,0,1]  # dots 1 and 8 on
char = chr(0x2800 + sum((1<<i) for i,b in enumerate(bits) if b))
print(char)