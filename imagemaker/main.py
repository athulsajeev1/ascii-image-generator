INPUT_FILE = "image2.bmp"
NEW_WIDTH = 120

# ASCII brightness ramp (dark → light)
ASCII_CHARS = "@#%*+=-:. "


# Read BMP

with open(INPUT_FILE, "rb") as f:
    bmp = bytearray(f.read())

data_offset = int.from_bytes(bmp[10:14], "little")
width = int.from_bytes(bmp[18:22], "little", signed=True)
height = int.from_bytes(bmp[22:26], "little", signed=True)
bpp = int.from_bytes(bmp[28:30], "little")

abs_height = abs(height)
bottom_up = height > 0

# Pixel size
if bpp == 24:
    bpp_bytes = 3
elif bpp == 32:
    bpp_bytes = 4
else:
    raise ValueError("Only 24/32-bit BMP supported")

row_size = (width * bpp_bytes + 3) & ~3


# Resize (aspect ratio corrected for ASCII)

aspect_correction = 0.55
scale = NEW_WIDTH / width
NEW_HEIGHT = int(abs_height * scale * aspect_correction)

# Convert to ASCII

ascii_image = []

for y in range(NEW_HEIGHT):
    src_y = int(y / (scale * aspect_correction))
    src_y = min(src_y, abs_height - 1)

    row = ""

    for x in range(NEW_WIDTH):
        src_x = int(x / scale)
        src_x = min(src_x, width - 1)

        index = data_offset + src_y * row_size + src_x * bpp_bytes

        b = bmp[index]
        g = bmp[index + 1]
        r = bmp[index + 2]

        # True luminance
        gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)

        # Map to ASCII
        char_index = gray * (len(ASCII_CHARS) - 1) // 255
        row += ASCII_CHARS[char_index]

    ascii_image.append(row)


# Fix BMP bottom-up orientation

if bottom_up:
    ascii_image.reverse()


# Print ASCII

print("\n===== ASCII OUTPUT =====\n")
for line in ascii_image:
    print(line)
