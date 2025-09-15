from PIL import Image

# Ouvre l'image existante
nom_img=input("nom de l'immage(.png): ")
img = Image.open(nom_img).convert("RGB")

# Parameters
width, height = 20, 10
img = Image.new("RGB", (width, height), "white")

# Message to hide
message = input('message caché :  ')
msg_bytes = message.encode('utf-8')  # ENCODAGE UTF-8 ICI !
msg_length = len(msg_bytes)

# --- 1. Encode message length in first 5 pixels' LSBs (15 bits) ---
bin_length = bin(msg_length)[2:].zfill(15)  # 15-bit binary string

for i in range(5):
    r, g, b = img.getpixel((0, i))
    for j in range(3):
        bit_index = i * 3 + j
        if bit_index < 15:
            bit = int(bin_length[bit_index])
            if j == 0:
                r = (r & ~1) | bit
            elif j == 1:
                g = (g & ~1) | bit
            else:
                b = (b & ~1) | bit
    img.putpixel((0, i), (r, g, b))

# --- 2. Encode the message (UTF-8 bytes) into LSBs of subsequent pixels ---
bits = "".join([bin(byte)[2:].zfill(8) for byte in msg_bytes])  # Message as bit string
bit_idx = 0
for y in range(height):
    for x in range(width):
        # Skip first 5 pixels in column 0
        if x == 0 and y < 5:
            continue
        r, g, b = img.getpixel((x, y))
        for j in range(3):
            if bit_idx < len(bits):
                bit = int(bits[bit_idx])
                if j == 0:
                    r = (r & ~1) | bit
                elif j == 1:
                    g = (g & ~1) | bit
                else:
                    b = (b & ~1) | bit
                bit_idx += 1
        img.putpixel((x, y), (r, g, b))

# Save the image
img.save(nom_img)
print("Image créée : ",nom_img)
