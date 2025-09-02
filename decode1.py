from PIL import Image, ImageDraw, ImageFont

# Load raw bytes from file
with open("tymponogram.log", "rb") as f:
    data = f.read()

bitmaps = []
i = 0

while i < len(data):
    if data[i:i+2] == b'\x1b\x4b':  # ESC K command
        mode = data[i+2]
        length = data[i+3] + (data[i+4]<<8)  # nL + nH*256
        bitmap = data[i+5:i+5+length]
        bitmaps.append(bitmap)
        i += 5 + length
    else:
        i += 1

# Flatten all bitmaps
bitmap_data = b''.join(bitmaps)

# Convert to pixels (8 pixels per byte)
pixels = []
for byte in bitmap_data:
    for bit in range(8):
        pixels.append(0 if (byte >> (7-bit)) & 1 else 255)  # 0=black, 255=white

# Assume printer width (adjust to your printer)
width = 384
height = len(pixels) // width
pixels = pixels[:width*height]

# Create image
img = Image.new('L', (width, height))
img.putdata(pixels)

# Optionally add text (example)
draw = ImageDraw.Draw(img)
# font = ImageFont.load_default()  # For ASCII text
# draw.text((0, 0), "ID: __________  DATE: 17Nov22", fill=0, font=font)

img.save("decoded_output.png")
img.show()
