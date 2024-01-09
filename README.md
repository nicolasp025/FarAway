# Projet Far Away

## Nicolas Potel - Nathan Signouret

#### Règles du jeu :
https://www.play-in.com/pdf/rules_games/faraway_-_regles_fr.pdf


#### UML :
https://lucid.app/lucidchart/f1e853e6-7e75-4ef3-9053-b722b3483ab9/edit?invitationId=inv_6565462c-3992-430f-b5cd-513f6364a41f


### Structure de données :
- Listes (Les cartes disponibles sur le plateau, les cartes sanctuaires des joueurs, ...)
- Piles (la main du joueur / la pioche)

### Algorithmie :
- Comptage des points (itération sur les cartes retournés et les cartes sanctuaires)
- Conséquence de l'action d'un joueur (détermination du nombre de cartes sanctuaires piochés par le joueur)
- Création de carte (Création de 68 cartes régions avec un numéro compris entre 1 et 68 et 45 cartes sancturaires)


## Cahier des charges :

Jeu avec interface graphique représentant le plateau de jeu, les cartes (sur le plateau et celles des joueurs).
Reproduction fidèle des règles du jeu.
Représentation des cartes par des objets, de même pour les joueurs et le plateau.

Algo comptage des points :
````
resultat = 0
Tant Que toutes les cartes ne sont pas retournées Faire
    carte = depile(cartes du joueur)
    Si pierres requises de la carte == Vrai alors
        resultat += bonus de la carte
    Fin Si
Fin Tant Que
Pour chaque carte sanctuaire du joueur Faire
    Si pierres requises de la carte == Vrai alors
        resultat += bonus de la carte
    Fin Si
Fin Pour
retourner resultat
```
