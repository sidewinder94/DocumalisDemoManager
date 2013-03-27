Installateur :
================================================================================
    Prérequis
================================================================================
- Visual Studio 2010 Professionnel

================================================================================
    Build Setup
================================================================================
- Ouvir le fichier "Application.sln" avec Visual Studio 2010
- Chercher la fenêtre "Solution Explorer"
- "replier" tous les éléments présents dans la fenetre (plus de visibilité)
- Clic droit sur "Documalis Demo Manager Install"
- Clic sur "Build"
- Attendre !

Demo Manager :
================================================================================
    Prérequis
================================================================================
- Microsoft .NET Framework 4
- IronPython (testé sous 2.7.3)

================================================================================
    Outils nécessaire au developpement
================================================================================
- Notepad (non-recommandé)
- Notepad++ (pour modification)
- Visual Studio (pour debug poussé & support autocompletion) (abrégé VS)
    Demande une version professionnelle pour installer des extensions
    Installation des outils python pour Visual Studio nécessaires (\\srvdata\Logiciels\IronPython\Visual Studio Tools)

================================================================================
    Installation d'IronPython
================================================================================
- Installer IronPython (\\srvdata\Logiciels\IronPython\IronPython-2.7.3.msi)

- Réaliser l' association de fichiers pour les type ".py" (en console)
    Clic droit sur un fichier d'extension .py en face de la ligne s'ouvre avec
         clique sur le bouton "modifier" -> "parcourir" et naviguer jusqu'au repertoire
         d'installation d'IronPython. Selectionner l'exécutable "ipy.exe" (exécution en console)

- Réaliser l' association de fichiers pour les type ".pyw" (fenétré)
    Mêmes étapes que ci-dessus mais sélectionner "ipyw.exe" à la place de "ipy.exe"

- Ajouter le repertoire d'IronPython au PATH de Windows
    - Accéder à l'interface Système ("Panneau de configuration" -> "Système")
        - Sous Windows XP cliquer sur l'onglet "Avancé" puis le bouton "Variables d'environnement"
        - Sous Windows 7 cliquer sur "Paramètres Systèmes Avancés" puis le bouton "Variables d'environnement"

    - Dans le cadre Variables Sytèmes selectionner Path puis cliquer sur modifier
         - Si un point virgule n'est pas présent a la fin du path en ajouter un
         - Ajouter  le chemin du répertoire contenant les exécutables "ipy.exe" et "ipyw.exe"

================================================================================
    Debug
================================================================================
- Avec IronPython : méthode la plus légère, ne nécessite pas l'install de VS
    - Ouvrir une console et se placer dans le dossier contenant l'application
    - taper "ipy" dans la console suivi du fichier a déboguer (ici : ipy main.pyw)
    - Utiliser la fonctionnalité a déboguer
    - Si un bogue apparait, l'application se fermera et la trace de l'exception s'affichera dans la console

- Avec VisualStudio
    - Ouvrir le fichier Application.pyproj avec Visual Studio
    - Placer les points d'arrets (falcultatif)
    - Cliquer sur le bouton démarrer OU Aller dans le menu déroulant Déboguer puis démarrer OU appuyer sur F5
    - Utiliser la fonctionnalité a déboguer
    - Une information sur l'exception soulevée sera indiquée au niveau de la fonction ayant appelée la fonction ayant appelé l'exception

L'avantage du débug en utilisant IronPython est la précision de la localisation de l'erreur
L'avantage du débug en utilisant VS est la possibilité de placer les points d'arrets, d'exécuter le code pas a pas,
de consulter l'état des variables en temps réel et de le modifier

La seule utilité du fichier debug.bat est de lancer le fichier main.txt en utilisant la version console d'IronPython

================================================================================
    Utilisation
================================================================================

Lancer le fichier main.pyw dans le dossier ou est placé le reste de l'appli
(Dans le cas où un raccourci à été crée penser a remplir le champ "Démarrer dans :")

Exemple : le Demo Manager est installé dans : "C:\Programmes\Demo Manager"
la cible du raccourci sera : "C:\Programmes\Demo Manager\main.pyw"
le champ "démarrer dans" aura la valeur : "C:\Programmes\Demo Manager\"