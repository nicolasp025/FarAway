# Projet Far Away

## Nicolas Potel - Nathan Signouret

#### Règles du jeu :
https://www.play-in.com/pdf/rules_games/faraway_-_regles_fr.pdf


#### UML :
https://lucid.app/lucidchart/f1e853e6-7e75-4ef3-9053-b722b3483ab9/edit?invitationId=inv_6565462c-3992-430f-b5cd-513f6364a41f

## Installation des modules
Pour jouer à Far Away, il vous faudra 2 modules de Python, que vous pouvez installer avec les commandes : ```pip install pygame``` et ```pip install pyg    ame-textinput```.


## Exécution :

Les commandes doivent être exécutées depuis le repertoire principal, pour exécuter le main : `make game` pour jouer depuis le terminal et `make` pour avoir une interface graphique (utilisation recommandée). Pour l'exécution des tests veuillez utilisez : `make tests` afin d'exécuter tout les tests à la suite.


## Structure de données :
- Listes (Les cartes disponibles sur le plateau, les cartes sanctuaires des joueurs, ...)
- Dictionnaires afin de stocker les ressources de chaques cartes retournées lors du comptage des points.
- Utilisation de fichiers json afin de créer chaque carte region et sanctuaire.

## Algorithmie :
- Comptage des points (à l'aide d'un dictionnaire et d'une mise à jour dynamique des points)
- Conséquence de l'action d'un joueur (détermination du nombre de cartes sanctuaires piochés par le joueur par exemple)
- Boucle de jeu


## Cahier des charges :
Jeu avec interface graphique (ou jouable sur le terminal) représentant le plateau de jeu, les cartes (sur le plateau et celles des joueurs) ainsi que les pioches.
Reproduction fidèle des règles du jeu.
Représentation des cartes par des objets, de même pour les joueurs et le plateau.


##### PyGame
Nous avons décidé d'utiliser la bibliothèque Pygame en Python afin de développer la partie graphique de ce projet pour plusieurs raisons. Tout d'abord, cette bibliothèque est largement utilisée pour le développement de jeux et de programmes interactifs, ce qui signifie que sa documentation est bien développée et que de nombreux exemples sont disponibles sur internet.

De plus, sa facilité d'utilisation nous a permis de nous concentrer davantage sur la programmation que sur la compréhension de Pygame elle-même. Elle nous a également permis de charger des images que nous avons souvent utilisées pour respecter au mieux les cartes de jeu physiques, ainsi que de créer des formes géométriques, d'afficher du texte et de permettre à l'utilisateur d'entrer du texte.


##### Déroulement d'une partie (simplifié)
Une partie se déroule en 8 tours.

Chaque tour se déroule en 3 phases :
- Chaque joueur choisit une carte parmi celles de sa main et la révèle.

- Chaque joueur peut choisir une carte sanctuaire si la carte région précédemment révélée est inférieure à celle qui vient d'être révélée.

- Chaque joueur choisit une carte à ajouter à sa main.

Enfin, à la fin des 8 tours, les points sont comptés en fonction des quêtes de chaque carte.




##### Avancement du projet
- Développement de l'architecture du projet et des structures de données à l'aide d'un diagramme UML.

- Début du développement des cartes et des quêtes, des joueurs, et enfin du plateau de jeu.

- En parrallèle, développement de tests unitaires.

- Finalisation de la première version jouable sur le terminal avec un affichage simple et correction des bugs.

- Création de tests simulant un scénario d'usage du jeu (simulation sur plusieurs tours de jeu).

- Début du développement de l'interface graphique, principalement apprentissage de la bibliothèque PyGame.

- Représentation graphique des cartes, ajout de l'intéractivité, boucle de jeu, information sur l'état de la partie, etc...

- Amélioration de l'affichage (fond d'écran, visualisation lors du survol d'une carte, scores, etc..)

- Correction de l'affichage en fonction de la taille de l'écran.

- Ajout de l'affichage des pioches ainsi que l'animation des cartes.



##### Possibles améliorations
- Affichage plus intelligent (charger chaque objet / image dans des variables au début du jeu afin d'éviter le chargement à chaque frame).

- Animation lors du comptage des points.

- Refactoring.