import PIL.Image

# ouverture du fichier :
img = PIL.Image.open('james_bond.png')

# lecture dans le fichier de la taille de l'image
largeur, hauteur = img.size

def taille_du_message():
    # Lecture et recuperation des R,V,B des 5 premiers pixels
    taille = []
    for i in range(5):
        r, v, b = img.getpixel((0, i))
        taille += [r, v, b]

    # passage R,V,B vers binaire et lecture bit caché
    bin_length = ""
    for i in range(len(taille)):
        x = bin(taille[i])
        bin_length += str(x[-1])
    
    length = int(bin_length, 2)
    return length

def lecture_des_RVB_du_message():
    ## Lecture et recuperation des R,V,B des pixels contenant le message
    msg_length = taille_du_message()
    total_pixels = []
    for h in range(hauteur):
        row = []
        for l in range(largeur):
            r, v, b = img.getpixel((l, h))
            row.append([r, v, b])
        total_pixels.append(row)

    # Enlever les 5 premiers pixels utilisés pour la taille
    for i in range(5):
        total_pixels[0].pop(0)

    return total_pixels, msg_length

def extraction_texte_depuis_bits_failbles(total_pixels, msg_length):
    bin_trad = ""
    count = 0
    # On parcourt la liste de pixels, on extrait le LSB de R, V, B (sauf les 5 premiers)
    for row in total_pixels:
        for pixel in row:
            for couleur in pixel:
                bin_trad += str(couleur & 1)
                count += 1
                if count >= msg_length * 8:
                    break
            if count >= msg_length * 8:
                break
        if count >= msg_length * 8:
            break

    # Découpe en octets de 8 bits
    octets = [bin_trad[i:i+8] for i in range(0, len(bin_trad), 8)]
    texte = "".join([chr(int(octet, 2)) for octet in octets if len(octet) == 8])
    print("Le message est :", texte)

total_pixels, msg_length = lecture_des_RVB_du_message()
extraction_texte_depuis_bits_failbles(total_pixels, msg_length)
