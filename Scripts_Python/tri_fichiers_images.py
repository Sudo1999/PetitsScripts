import os    # os est historiquement la bibliothèque de manipulation du système de fichiers (os.listdir, os.rename, os.path.join…). Mais ici elle est importée sans être utilisée — tout est fait avec pathlib.
from pathlib import Path    # Au lieu d'importer tout le module 'pathlib' comme pour les autres imports, la syntaxe permet d'en cibler un élément précis et de le rendre directement disponible. La classe Path du module pathlib représente les chemins de fichiers de façon objet.
import shutil    # Quand on importe tout le module comme ici avec shutil, pour utiliser une fonction, il faut la précéder du nom du module, par exemple shutil.move(), qui déplace un fichier d'un dossier vers un autre.
import sys
import re
import time

#### Fonctions ####
###################

def suffixes_presents(dossier):
  suffixes = set()    # (un set évite les doublons)
  for fichier in dossier.iterdir():
    if not fichier.is_file():
      continue
    
    stem = fichier.stem    # (stem fournit le nom du fichier sans son extension)
    end = re.search(r"_(\d+)$", stem)
    if end:
      suffixes.add(end.group(0))    # "_20", "_40", ... (end.group(0) renvoie le match complet) 
    else:
      if fichier.stem.endswith("_compressed"):
        suffixes.add("_compressed")
  
  return sorted(suffixes)

def application_regle_1(dossier, suffixes):
  classement = {
    "_compressed": "Fichiers_80",
    }
  for suffixe in suffixes:
    if suffixe not in classement:
      classement[suffixe] = f"Fichiers{suffixe}"    # "_20" -> "Fichiers_20"
  
  for fichier in dossier.iterdir():
    if not fichier.is_file():
      print(f"{fichier} n'est pas un fichier")    # f = formatted string literal, remplace la variable spécifiée par sa valeur
      continue
    
    for suffixe, sous_dossier in classement.items():    # La boucle for... in fait de marqueur une clé, et de sous_dossier sa valeur.
      stem = fichier.stem
      if stem.endswith(suffixe):
        destination = dossier / sous_dossier
        destination.mkdir(exist_ok=True)
        shutil.move(str(fichier), str(destination / fichier.name))    # fichier.name = fichier.stem + fichier.suffix
        print(f"{fichier.name} -> {sous_dossier}/")
        break

def application_regle_2(dossier, suffixes):
  choix_action = dict.fromkeys(suffixes)
  choix_action["originaux"] = None
  
  print("Attention, la suppression est définitive. Veuillez confirmer :")
  for suffixe in choix_action:
    choix = input(f"Voulez-vous supprimer les fichiers {suffixe} ? Si oui entrez O, sinon entrez N : ").upper()
    if ((choix != 'O') & (choix != 'N')):
      choix = input(f"Choix invalide. Veuillez recommencer. \nVoulez-vous conserver ces fichiers ? Si oui entrez O, sinon entrez N : ").upper()
    if ((choix != 'O') & (choix != 'N')):
      choix = 'N'
    choix_action[suffixe] = choix
  
  for fichier in dossier.iterdir():
    if not fichier.is_file():
      print(f"{fichier} n'est pas un fichier")
      continue
    
    stem = fichier.stem
    original = True
    for suffixe, choix in choix_action.items():
      if (stem.endswith(suffixe)):
        original = False
        if (choix == 'N'):
          break
        if (choix == 'O'):
          fichier.unlink()
          print(f"{fichier.name} supprimé.")
          break
    
    if original:
      if choix_action['originaux'] == 'N':
        continue
      if choix_action['originaux'] == 'O':
        fichier.unlink()
        print(f"{fichier.name} supprimé.")
        continue

#### Répertoire de travail ####
###############################

saisie = input("Entrez le chemin du dossier, ou Entrée pour le dossier par défaut : ")
if (not saisie):
  saisie = r"C:\Dossiers\Telechargement\Transfert"            # r = raw string = chaîne brute

DOSSIER = Path(saisie)
if not DOSSIER.is_dir():
  input(f"Erreur : le dossier '{DOSSIER}' est introuvable. Appuyez sur la touche Entrée...")
  sys.exit()
print("Vous êtes dans le dossier " + saisie)

#### Règle à appliquer ####
###########################

regle = input("Entrez 1 pour le tri des fichiers, ou 2 pour la supression des fichiers redondants : ")
print(f"{'La règle 1 va être appliquée.' if regle == '1' else 'La règle 2 va être appliquée.' if regle == '2' else 'Aucune règle valide ne se trouve sélectionnée.'}")
if (not regle):
  regle = input("Entrez 1 pour le tri des fichiers, ou 2 pour la supression des fichiers redondants : ")
  print(f"{'La règle 1 va être appliquée.' if regle == '1' else 'La règle 2 va être appliquée.' if regle == '2' else 'Aucune règle valide ne se trouve sélectionnée. Le programme va se fermer dans cinq secondes.'}")
  time.sleep(5)
  sys.exit()

ACTIVER_REGLE_1 = (regle == '1')
ACTIVER_REGLE_2 = (regle == '2')

SUFFIXES = suffixes_presents(DOSSIER)

#### Mise en oeuvre ####
########################

if ACTIVER_REGLE_1:
  application_regle_1(DOSSIER, SUFFIXES)

if ACTIVER_REGLE_2:
  application_regle_2(DOSSIER, SUFFIXES)

input("Appuyez sur la touche Entrée...")