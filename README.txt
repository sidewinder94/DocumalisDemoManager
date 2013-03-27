Installateur :
================================================================================
    Pr�requis
================================================================================
- Visual Studio 2010 Professionnel

================================================================================
    Build Setup
================================================================================
- Ouvir le fichier "Application.sln" avec Visual Studio 2010
- Chercher la fen�tre "Solution Explorer"
- "replier" tous les �l�ments pr�sents dans la fenetre (plus de visibilit�)
- Clic droit sur "Documalis Demo Manager Install"
- Clic sur "Build"
- Attendre !

Demo Manager :
================================================================================
    Pr�requis
================================================================================
- Microsoft .NET Framework 4
- IronPython (test� sous 2.7.3)

================================================================================
    Outils n�cessaire au developpement
================================================================================
- Notepad (non-recommand�)
- Notepad++ (pour modification)
- Visual Studio (pour debug pouss� & support autocompletion) (abr�g� VS)
    Demande une version professionnelle pour installer des extensions
    Installation des outils python pour Visual Studio n�cessaires (\\srvdata\Logiciels\IronPython\Visual Studio Tools)

================================================================================
    Installation d'IronPython
================================================================================
- Installer IronPython (\\srvdata\Logiciels\IronPython\IronPython-2.7.3.msi)

- R�aliser l' association de fichiers pour les type ".py" (en console)
    Clic droit sur un fichier d'extension .py en face de la ligne s'ouvre avec
         clique sur le bouton "modifier" -> "parcourir" et naviguer jusqu'au repertoire
         d'installation d'IronPython. Selectionner l'ex�cutable "ipy.exe" (ex�cution en console)

- R�aliser l' association de fichiers pour les type ".pyw" (fen�tr�)
    M�mes �tapes que ci-dessus mais s�lectionner "ipyw.exe" � la place de "ipy.exe"

- Ajouter le repertoire d'IronPython au PATH de Windows
    - Acc�der � l'interface Syst�me ("Panneau de configuration" -> "Syst�me")
        - Sous Windows XP cliquer sur l'onglet "Avanc�" puis le bouton "Variables d'environnement"
        - Sous Windows 7 cliquer sur "Param�tres Syst�mes Avanc�s" puis le bouton "Variables d'environnement"

    - Dans le cadre Variables Syt�mes selectionner Path puis cliquer sur modifier
         - Si un point virgule n'est pas pr�sent a la fin du path en ajouter un
         - Ajouter  le chemin du r�pertoire contenant les ex�cutables "ipy.exe" et "ipyw.exe"

================================================================================
    Debug
================================================================================
- Avec IronPython : m�thode la plus l�g�re, ne n�cessite pas l'install de VS
    - Ouvrir une console et se placer dans le dossier contenant l'application
    - taper "ipy" dans la console suivi du fichier a d�boguer (ici : ipy main.pyw)
    - Utiliser la fonctionnalit� a d�boguer
    - Si un bogue apparait, l'application se fermera et la trace de l'exception s'affichera dans la console

- Avec VisualStudio
    - Ouvrir le fichier Application.pyproj avec Visual Studio
    - Placer les points d'arrets (falcultatif)
    - Cliquer sur le bouton d�marrer OU Aller dans le menu d�roulant D�boguer puis d�marrer OU appuyer sur F5
    - Utiliser la fonctionnalit� a d�boguer
    - Une information sur l'exception soulev�e sera indiqu�e au niveau de la fonction ayant appel�e la fonction ayant appel� l'exception

L'avantage du d�bug en utilisant IronPython est la pr�cision de la localisation de l'erreur
L'avantage du d�bug en utilisant VS est la possibilit� de placer les points d'arrets, d'ex�cuter le code pas a pas,
de consulter l'�tat des variables en temps r�el et de le modifier

La seule utilit� du fichier debug.bat est de lancer le fichier main.txt en utilisant la version console d'IronPython

================================================================================
    Utilisation
================================================================================

Lancer le fichier main.pyw dans le dossier ou est plac� le reste de l'appli
(Dans le cas o� un raccourci � �t� cr�e penser a remplir le champ "D�marrer dans :")

Exemple : le Demo Manager est install� dans : "C:\Programmes\Demo Manager"
la cible du raccourci sera : "C:\Programmes\Demo Manager\main.pyw"
le champ "d�marrer dans" aura la valeur : "C:\Programmes\Demo Manager\"