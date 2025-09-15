from PIL import Image

# Ouverture du fichier image
nom_img=input("nom de l'immage(.png): ")
img = Image.open(nom_img).convert("RGB")
largeur, hauteur = img.size

def taille_du_message():
    # Récupère les LSB des R,G,B des 5 premiers pixels de la colonne 0
    bits = []
    for i in range(5):
        r, g, b = img.getpixel((0, i))
        for v in (r, g, b):
            bits.append(v & 1)
    bin_length = "".join(map(str, bits))
    return int(bin_length, 2)

def lecture_des_bits_du_message():
    msg_length = taille_du_message()
    bits = []
    count = 0
    for y in range(hauteur):
        for x in range(largeur):
            # Ignore les 5 premiers pixels de la colonne 0
            if x == 0 and y < 5:
                continue
            r, g, b = img.getpixel((x, y))
            for v in (r, g, b):
                if count < msg_length * 8:
                    bits.append(v & 1)
                    count += 1
                else:
                    break
            if count >= msg_length * 8:
                break
        if count >= msg_length * 8:
            break
    return bits, msg_length

def extraction_texte_utf8(bits, msg_length):
    # Regroupe les bits en octets
    octets = [bits[i:i+8] for i in range(0, len(bits), 8)]
    byte_values = [int("".join(map(str, octet)), 2) for octet in octets if len(octet) == 8]
    try:
        message = bytes(byte_values).decode('utf-8')
        print("Le message est :", message)
    except UnicodeDecodeError as e:
        print("Erreur de décodage UTF-8 :", e)
        print("Octets extraits :", byte_values)

bits, msg_length = lecture_des_bits_du_message()
extraction_texte_utf8(bits, msg_length)
