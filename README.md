# DEMINEUR INFINI
> Le Démineur (Minesweeper) est un jeu vidéo de réflexion dont le but est de localiser des mines cachées dans une grille représentant un champ de mines virtuel, avec pour seule indication le nombre de mines dans les zones adjacentes.<br /> *Source : [Article Démineur (genre de jeu vidéo) de Wikipédia en français](https://fr.wikipedia.org/wiki/D%C3%A9mineur_(genre_de_jeu_vid%C3%A9o)).*

On va essayer de se rapprocher le plus possible de cette définition en rajoutant une grille infinie et d'autres fonctionalitée.
## Fonctionnalités:
### Obligatoire:
- Génération des mines et cases a l'infini de manière procédurale (permet de ne pas tout charger/stocker)
- Stockage de la progression du joueur de manière optimisée
- Système de score
- Menu (accueil, pause, paramètres...)
- Paramètres (thème, difficulté)
### Intermédiaires:
- Système de biomes dans lesquels les règles sont différentes : 2 à 3 mines par case, plus de chances de mines…
### Bonus:
- Objets permettant de modifier le jeu : outils pour sonder des cases, reboucher des mines…
- Multijoueur
- Machine learning pour déterminer le niveau des joueurs automatiquement et adapter le démineur automatiquement (plus ou moins de difficulté).
## Outils utilisés:
- Python 3.14 avec les modules requests et random
- [Pygame](https://www.pygame.org)
