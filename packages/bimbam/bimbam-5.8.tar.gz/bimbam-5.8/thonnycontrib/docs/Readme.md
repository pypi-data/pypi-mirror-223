# Internationalisation du plugin

## Introduction
Afin de prendre en charge l'internationalisation des textes utilisés par le plugin, suivez attentivement les étapes décrites dans ce guide.

## Utilisation de la méthode `tr()`
1. Intégration dans le code : Tous les textes qui doivent être traduits doivent utiliser la méthode `tr()` provenant du module `i18n/languages.py`. Assurez-vous de consulter les exemples d'utilisation dans le code source existant avant d'intégrer cette méthode dans vos propres modules.

2. Mise à jour des traductions : Exécutez le script `update_i18n.sh`. Ce script mettra à jour le fichier template `.pot` en y ajoutant les nouveaux termes issus de votre code.

    En situant à la racine (/thonnycontrib), vous lancez :
    ```bash
    ./update_i18n.sh
    ```

## Création et édition des fichiers `.po`
1. Création du fichier `.po` : Copiez le fichier `.pot` mis à jour et renommez-le avec l'extension `.po`.

2. Édition de l'en-tête : Modifiez l'en-tête du fichier `.po` pour qu'il ressemble à :

    ```bash
    msgid ""
    msgstr ""
    "MIME-Version: 1.0\n"
    "Content-Type: text/plain; charset=UTF-8\n"
    "Content-Transfer-Encoding: 8bit\n"
    "X-Generator: POEditor.com\n"
    "Project-Id-Version: l1test\n"
    "Language: fr\n"
    ```
3. Emplacement des fichiers : Assurez-vous que tous les fichiers `.po` sont placés dans le répertoire suivant : `i18n/locale/xx_XX/LC_MESSAGES`. Le xx_XX représente le code de la langue et du pays (par exemple fr_FR pour le français de France).

## Compilation des traductions
1. Compilation : Pour compiler vos fichiers `.po` en fichiers `.mo`, exécutez simplement le script `compile_translations.sh`. 

    En situant à la racine (/thonnycontrib), vous lancez :
    ```bash
    ./compile_translations.sh
    ```

2. Résultat : Les fichiers `.mo` générés seront placés dans les sous-répertoires appropriés de /locale. Ces fichiers binaires `.mo` sont utilisés en temps réel par la bibliothèque de traduction gettext.

## Conclusion
En suivant ces étapes, vous garantissez une prise en charge correcte de l'internationalisation pour votre plugin. Merci de vous assurer que chaque texte destiné à l'utilisateur utilise la méthode `tr()` afin de garantir une expérience utilisateur cohérente dans toutes les langues.