# Script pour débarrasser automatiquement le texte d'un bloc-note de certains caractères
# (par exemple ZWSP ZWNJ et WJ) :

import sys  # Le module sys fournit un accès à des fonctionnalités du système
import re   # Le module re (regex) permet d'utiliser re.sub
import json

# Caractères à supprimer
REMOVE_CHARS = {
    "\u200B",  # ZWSP (Zero Width Space) en encodage Javascript (​	U+200B	Espace sans chasse en Unicode)
    "\u200C",  # ZWNJ (Zero Width Non-Joiner) en encodage Javascript (‌	U+200C	Antiliant sans chasse en Unicode)
    "\u200E",  # LRM (Left-To-Right Mark) en encodage Javascript (‎	U+200E	Marque gauche-à-droite en Unicode)
    "\u2060",  # WJ (Word Joiner) en encodage Javascript (⁠	U+2060	Gluon de mots en Unicode)
}

# Remplacements typographiques
with open("replacements.json", "r", encoding="utf-8") as f:  # with crée un gestionnaire de contexte garantissant la fermeture automatique
                                                             # de la ressource après son utilisation, même en cas d'erreur.
    REPLACEMENTS = json.load(f)
TABLE = str.maketrans(REPLACEMENTS)


def clean_text(text):
    # 1. Supprimer les caractères invisibles
    text = "".join(c for c in text if c not in REMOVE_CHARS)

    # 2. Remplacer les caractères listés dans la fonction
    text = text.translate(TABLE)

    # 3. Remplacer deux CRLF consécutifs par un seul
    # (L'ouverture de texte par défaut sur Windows convertit \r\n en \n à la lecture, et refait l’inverse à l’écriture)
    text = re.sub(r'(?:\n){2,}', '\n', text)

    # 4. Supprimer le premier saut de ligne ainsi que le premier espace si le texte commmence par un de ces caractères
        # (text.lstrip() supprime tous les types d'espaces invisibles en début de texte (l= left) :
        # l'espace, le saut de ligne (\n), la tabulation (\t) et le retour chariot (\r))
    #text = re.sub(r'^\n+', '', text)
    #text = re.sub(r'^ +', '', text)
    text = text.lstrip()

    # 5. Supprimer les espaces non précédés d'un point avant un CRLF
    text = re.sub(r'(?<!\.) +\n', '\n', text)
    
    # 6. Ajouter un point avant tout CRLF non déjà précédé d'un point
    text = re.sub(r'(?<!\.)\n', '.\n', text)

    # 7. Ajouter un espace entre le points et le CRLF
    text = re.sub(r'\.\n', '. \n', text)

    # 8. Supprimer l'espace et le saut de ligne après le point à la dernière ligne
        # (text.rstrip() supprime tous les types d'espaces invisibles en fin de texte (r = right) :
        # l'espace, le saut de ligne (\n), la tabulation (\t) et le retour chariot (\r))
    #text = text.rstrip(" \n")
    text = text.rstrip()
    
    return text

def main(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()

    cleaned = clean_text(content)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(cleaned)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python clean_text.py input.txt output.txt")
        input("Appuyez sur la touche Entrée...")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2])

# Usage :
# python clean_text.py Courrier_International.txt Clean_Text.txt

