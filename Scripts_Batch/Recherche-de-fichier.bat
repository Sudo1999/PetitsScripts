@echo off
chcp
set /p fichierRecherche=Entrez le nom du fichier à rechercher (ex: Accès Copie.png) : 
set /p cheminRecherche=Entrez le dossier dans lequel lancer la recherche (ex: C:\Dossiers) : 
dir /s /b "%cheminRecherche%\%fichierRecherche%"

:: /p (p pour prompt) : Il sert à demander une saisie à l'utilisateur.
:: /s (s pour subdirectories) : La recherche s’effectue dans tous les sous-dossiers.
:: /b (b pour bare format) : Le dir liste uniquement le chemin d'accès brut, dépourvu de toutes les autres informations de date, de taille etc.

pause
