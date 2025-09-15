from PIL import Image

# Ouvre l'image existante
nom_img = input("nom de l'image (.png): ")
img = Image.open(nom_img).convert("RGB")

# Récupère la taille de l'image existante
width, height = img.size

# Message à cacher
message = input('message caché : ')
msg_bytes = message.encode('utf-8')  # ENCODAGE UTF-8
msg_length = len(msg_bytes)

if width * height * 3 < 15 + msg_length * 8:
    print("Image trop petite pour cacher ce message !")
    exit()

# --- 1. Encode la taille du message dans les 5 premiers pixels de la colonne 0 ---
bin_length = bin(msg_length)[2:].zfill(15)  # 15 bits pour la taille

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

# --- 2. Encode le message (UTF-8 bytes) dans les LSBs des pixels suivants ---
bits = "".join([bin(byte)[2:].zfill(8) for byte in msg_bytes])
bit_idx = 0
for y in range(height):
    for x in range(width):
        # Saute les 5 premiers pixels de la colonne 0
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
        if bit_idx >= len(bits):
            break
    if bit_idx >= len(bits):
        break

# Sauvegarde l'image modifiée sous le même nom
img.save(nom_img)
print("Message caché dans l'image :", nom_img)
