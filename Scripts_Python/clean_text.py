# Script pour débarrasser automatiquement le texte d'un bloc-note de certains caractères
# (par exemple ZWSP ZWNJ et WJ) :

import sys  # Le module sys fournit un accès à des fonctionnalités du système
import re   # Le module re (regex) permet d'utiliser re.sub

# Caractères à supprimer
REMOVE_CHARS = {
    "\u200B",  # ZWSP (Zero Width Space) en encodage Javascript (​	U+200B	Espace sans chasse en Unicode)
    "\u200C",  # ZWNJ (Zero Width Non-Joiner) en encodage Javascript (‌	U+200C	Antiliant sans chasse en Unicode)
    "\u200E",  # LRM (Left-To-Right Mark) en encodage Javascript (‎	U+200E	Marque gauche-à-droite en Unicode)
    "\u2060",  # WJ (Word Joiner) en encodage Javascript (⁠	U+2060	Gluon de mots en Unicode)
}

# Remplacements typographiques
REPLACEMENTS = {
    "\u00A0": " ",  # NBSP (Non-Breaking Space) en encodage Javascript ( 	U+00A0	Espace insécable en Unicode)
    "‘": "'",    # guillemet-apostrophe culbuté (U+2018) → apostrophe dactylographique (Code ASCII 39 = Unicode U+0027)
    "’": "'",    # apostrophe typographique (U+2019) → apostrophe dactylographique (Code ASCII 39 = Unicode U+0027)
                 #   ((( apostrophe typographique = guillemet-apostrophe )))
    "“": '"',    # guillemet ouvrant typographique (U+201C) → guillemet dactylographique " (Code ASCII 34 = Unicode U+0022)
                 #   ((( guillemet ouvrant typographique = guillemet-apostrophe double culbuté )))
    "”": '"',    # guillemet fermant typographique (U+201D) → guillemet dactylographique " (Code ASCII 34 = Unicode U+0022)
                 #   ((( guillemet fermant typographique = guillemet-apostrophe double )))
    "«": '"',    # guillemet gauche (U+00AB) → guillemet dactylographique " (Code ASCII 34 = Unicode U+0022)
    "»": '"',    # guillemet droit (U+00BB) → guillemet dactylographique " (Code ASCII 34 = Unicode U+0022)
    '–': '-',    # tiret demi-cadratin (U+2013 = E2 80 93 en UTF-8) → tiret simple (Code ASCII 45 = Unicode U+002D)
    '—': '-',    # tiret cadratin (	U+2014 = E2 80 94 en UTF-8) → tiret simple (Code ASCII 45 = Unicode U+002D)
    '−': '-',    # signe moins (U+2212 = E2 88 92 en UTF-8) → tiret simple (Code ASCII 45 = Unicode U+002D)
                 #   ((( tiret simple = trait d'union-signe moins )))
    'œ': 'oe',   # (œ = U+0153 en Unicode, \u0153 en encodage Javascript, absent en ASCII et en ISO-8859-1, 
                 #   mais présent (0xBD) en ISO-8859-15, 0xC5 0x93 en UTF-8, 0x0153 en UTF-16)
    'À': 'A',    # (À = U+00C0 en Unicode)
    'Â': 'A',    # (Â = U+00C2 en Unicode)
    'È': 'E',    # (È = U+00C8 en Unicode)
    'É': 'E',    # (É = U+00C9 en Unicode)
    'Ê': 'E',    # (Ê = U+00CA en Unicode)
    'Î': 'I',    # (Î = U+00CE en Unicode)
    'Ç': 'C',    # (Ç = U+00C7 en Unicode)
    'á': 'a',    # (á = U+00E1 en Unicode)
    'ã': 'a',    # (ã = U+00E3 en Unicode)
    'í': 'i',    # (í = U+00ED en Unicode)
    'ò': 'o',    # (ò = U+00F2 en Unicode)
    'ó': 'o',    # (ó = U+00F3 en Unicode)
    'ø': 'o',    # (ø = U+00F8 en Unicode)
    'ú': 'u',    # (ú = U+00FA en Unicode)
    'ñ': 'n',    # (ñ = U+00F1 en Unicode)
    '…': '...',  # (… = U+2026 en Unicode)
}

def clean_text(text):
    # 1. Supprimer les caractères invisibles
    text = "".join(c for c in text if c not in REMOVE_CHARS)

    # 2. Remplacer les caractères listés dans la fonction
    for old, new in REPLACEMENTS.items():
        text = text.replace(old, new)

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