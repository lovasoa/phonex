# phonex

Port de l'algorithme phonex vers python3.
Permet de calculer un nombre qui correspond à la prononciation d'un mot en français.

[Voir la version originale](http://info.univ-lemans.fr/~carlier/recherche/soundex.html).


Phonex est un algorithme de Soundex plus perfectionné encore que la version francisée de Soundex2.
Sachez que Phonex est optimisée pour le langage français, sait reconnaître différents types de sons
comme les sons ‘on’, ‘ai’, ‘ein’, etc... et place son résultat sous la forme d’un réel de type double précision
(5.0 x 10-324 .. 1.7 x 10308 sur 15 à 16 chiffres significatifs).
Son temps de calcul est double de Soundex et 30% supérieure seulement à Soundex2.

Algorithme Phonex
Copyright Frédéric BROUARD (31/3/99)