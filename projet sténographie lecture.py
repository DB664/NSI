# Importation de la bibliothèque pour manipuler les images
from PIL import Image  

# Demande à l'utilisateur le nom du fichier image à ouvrir
nom_img = input("nom de l'immage(.png): ")

# Ouverture de l'image et conversion en mode RGB (3 couleurs)
img = Image.open(nom_img).convert("RGB")
# Récupération des dimensions de l'image
largeur, hauteur = img.size

def taille_du_message():
    """
    Cette fonction lit les LSB (Least Significant Bit = bit de poids faible)
    des composantes R, V, B des 5 premiers pixels de la colonne 0 pour
    reconstituer la taille du message caché dans l'image.
    """
    bits = []
    # Parcourt les 5 premiers pixels de la colonne 0
    for i in range(5):  
        # Récupère les valeurs Rouge, Vert, Bleu
        r, v, b = img.getpixel((0, i))  
        # Pour chaque couleur du pixel
        for y in (r, v, b):  
            # Ajoute le LSB (bit de poids faible) à la liste
            bits.append(y & 1)  
    # Transforme la liste de bits en chaîne de caractères binaire
    bin_length = "".join(map(str, bits)) 
    # Convertit la chaîne binaire en entier (base 2)
    return int(bin_length, 2)  

def lecture_des_bits_du_message():
    """
    Cette fonction extrait les bits du message caché dans l'image,
    en ignorant les 5 premiers pixels de la colonne 0 (utilisés pour la taille).
    """
    # Récupère la taille du message en octets
    msg_length = taille_du_message()  
    bits = []

    # Compte le nombre de bits lus
    count = 0  
    # Parcourt toutes les lignes
    for y in range(hauteur):  
        # Parcourt toutes les colonnes
        for x in range(largeur):  
            # Ignore les 5 premiers pixels de la colonne 0
            if x == 0 and y < 5:
                continue
            # Récupère les valeurs RGB du pixel
            r, v, b = img.getpixel((x, y))  
            # Pour chaque couleur
            for e in (r, v, b):  
                # S'il reste des bits à lire
                if count < msg_length * 8:  
                    # Ajoute le LSB à la liste
                    bits.append(e & 1)  
                    count += 1
                else:
                    # Arrête si tous les bits ont été lus
                    break  
            if count >= msg_length * 8:
                break
        if count >= msg_length * 8:
            break
    # Retourne la liste des bits et la taille du message
    return bits, msg_length  

def extraction_texte_utf8(bits, msg_length):
    """
    Cette fonction regroupe les bits extraits en octets (8 bits),
    puis tente de les décoder en texte UTF-8 pour obtenir le message caché.
    """
    # Regroupe les bits par 8
    octets = [bits[i:i+8] for i in range(0, len(bits), 8)]  
    # Transforme chaque groupe de 8 bits en entier
    byte_values = [int("".join(map(str, octet)), 2) for octet in octets if len(octet) == 8]  
    try:
        # Tente de décoder les octets en texte UTF-8
        message = bytes(byte_values).decode('utf-8')  
        # Affiche le message si la conversion réussit
        print("Le message est :", message)  
        # Si la conversion échoue
    except UnicodeDecodeError as e:  
        print("Erreur de décodage UTF-8 :", e)
        # Affiche les octets bruts
        print("Octets extraits :", byte_values)  

# Appel des fonctions pour extraire le message
bits, msg_length = lecture_des_bits_du_message() 
extraction_texte_utf8(bits, msg_length)
