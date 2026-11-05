@echo off
REM Par défaut, un script batch affiche chaque commande avant de l'exécuter.
REM La commande « @echo off » supprime cet affichage et rend le script beaucoup plus lisible.

chcp 65001 1>nul

REM (REM = Remark) :
REM En batch, il existe plusieurs flux (streams) d'entrée/sortie.
REM Par défaut :
REM 0 = entrée standard (stdin)
REM 1 = sortie standard (stdout)
REM 2 = sortie d'erreur (stderr)

:: "chcp 65001 >nul" est un raccourci vers "chcp 65001 1>nul".
:: Il redirige la sortie standard vers le périphérique spécial nul, qui joue le rôle de la "corbeille".
:: Le message "Page de codes active : 65001" est produit sur stdout et disparaît.
:: (Celui qui s'affiche provient du script suivant, Recherche de fichier.bat)

set /p fichierExecutable=Entrez le nom du script à exécuter (Exemple Recherche de fichier.bat) : 
call "%fichierExecutable%"