
# Ce script analyse chaque dossier à la racine de Temp. Il ne supprime un dossier que si tout son contenu (fichiers et sous-dossiers inclus) est plus ancien que le délai choisi. Il ignore automatiquement les fichiers verrouillés sans faire planter le système.

# ================================================
# Standardisation préliminaire de l'encodage
# ================================================

## Correctif des erreurs d'affichage dans la console ((Equivalent de la commande chcp 65001 dans un script batch)
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

## Pour la lecture de fichiers texte (.txt, .log, etc.) entrants, $OutputEncoding n'intervient pas. C'est le paramètre -Encoding de la commande de lecture qui dicte la règle. Si les fichiers texte sont en UTF-8, PowerShell moderne (v7+) les lit en UTF-8 par défaut. Sur l'ancien Windows PowerShell (v5.1), il vaut mieux forcer la lecture en ajoutant -Encoding UTF8.
## Exemple : Get-Content -Path "mon_fichier.txt" -Encoding UTF8

## Pour exécuter le script manuellement via le boîtier Exécuter de Windows (-NoExit maintient la fenêtre ouverte) :
# powershell -NoExit -NoProfile -ExecutionPolicy Bypass -File "C:\Users\Martine\Documents\Scripts Powershell\NettoyerTemp.ps1"

# ==========================================================================
# CONFIGURATION : Définissez ici l'ancienneté requise (ex: 14 ou 30 jours)
# ==========================================================================

$DelaiJours = 14
$DateLimite = (Get-Date).AddDays(-$DelaiJours)
$CheminTemp = "$env:USERPROFILE\AppData\Local\Temp"

Write-Host "Début du nettoyage du dossier Temp de $env:USERPROFILE (Éléments plus vieux que $DelaiJours jours)..."

# 1. Traitement des éléments directement à la racine de Temp
Get-ChildItem -Path $CheminTemp | ForEach-Object {
    $Element = $_
    
    # CAS A : C'est un fichier isolé
    if ($Element.PSIsContainer -eq $false) {
        if ($Element.LastWriteTime -lt $DateLimite) {
            Remove-Item -Path $Element.FullName -ErrorAction SilentlyContinue
        }
    }
    # CAS B : C'est un dossier
    else {
        # On cherche l'élément le plus récent à l'intérieur de ce dossier
        $ContenuPlusRecent = Get-ChildItem -Path $Element.FullName -Recurse -ErrorAction SilentlyContinue | 
                             Sort-Object LastWriteTime -Descending | 
                             Select-Object -First 1

        # Si le dossier est totalement vide OU si son élément le plus récent est plus vieux que la limite
        if ($ContenuPlusRecent -eq $null -or $ContenuPlusRecent.LastWriteTime -lt $DateLimite) {
            # On supprime le dossier et tout son contenu (sans forcer les fichiers verrouillés)
            Remove-Item -Path $Element.FullName -Recurse -ErrorAction SilentlyContinue
        }
    }
}

Write-Host "Nettoyage terminé."