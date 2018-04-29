#!/bin/python
# -*- coding: UTF-8 -*-

# Origine : Algorithme Phonex de Frédéric BROUARD (31/3/99)
# Source : http://sqlpro.developpez.com/cours/soundex
# Version Python : Christian Pennaforte - 5 avril 2005
# Suite : Florent Carlier
# Adaptation Python 3: Ophir LOJKINE

import re
import unicodedata

def remove_accents(input_str):
    """
    >>> remove_accents("héhé")
    "hehe
    """
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii.decode("utf8")

def phonex(chaine):
    """Phonex est un algorithme de Soundex plus perfectionné encore que la version francisée de Soundex2.
    Sachez que Phonex est optimisée pour le langage français, sait reconnaître différents types de sons comme les sons
    ‘on’, ‘ai’, ‘ein’, etc...
    et place son résultat sous la forme d’un réel de type double précision (5.0 x 10-324 .. 1.7 x
    10308 sur 15 à 16 chiffres significatifs). Son temps de calcul est double de Soundex et 30% supérieure seulement
    à Soundex2.

    >>> phonex("PHYLAURHEIMSMET")
    0.29241361598339205

    :param chaine: La chaine de caractères à encoder
    :return: L'encodage sous forme de nombre à virgule flottante
    """
    # 0 On met la chaîne en majuscules, on vire les caractères parasites
    chaine = remove_accents(chaine)
    chaine = re.sub(r"[ \-.+*/,:;_']", "", chaine)
    chaine = chaine.upper()

    # 1 remplacer les y par des i
    r = chaine.replace('Y', 'I')

    # 2 supprimer les h qui ne sont pas précédées de c ou de s ou de p
    r = re.sub(r'([^PCS])H', r'\1', r)

    # 3 remplacement du ph par f
    r = r.replace(r'PH', r'F')

    # 4 remplacer les groupes de lettres suivantes :
    r = re.sub(r'G(AI?[NM])', r'K\1', r)

    # 5 remplacer les occurrences suivantes, si elles sont suivies par une lettre a, e, i, o, ou u :
    r = re.sub(r'[AE]I[NM]([AEIOU])', r'YN\1', r)

    # 6 remplacement de groupes de 3 lettres (sons 'o', 'oua', 'ein') :
    r = r.replace('EAU', 'O')
    r = r.replace('OUA', '2')
    r = r.replace('EIN', '4')
    r = r.replace('AIN', '4')
    r = r.replace('EIM', '4')
    r = r.replace('AIM', '4')

    # 7 remplacement du son É:
    r = r.replace('É', 'Y')  # CP : déjà fait en étape 0
    r = r.replace('È', 'Y')  # CP : déjà fait en étape 0
    r = r.replace('Ê', 'Y')  # CP : déjà fait en étape 0
    r = r.replace('AI', 'Y')
    r = r.replace('EI', 'Y')
    r = r.replace('ER', 'YR')
    r = r.replace('ESS', 'YS')
    r = r.replace('ET', 'YT')  # CP : différence entre la version Delphi et l'algo
    r = r.replace('EZ', 'YZ')

    # 8 remplacer les groupes de 2 lettres suivantes (son â..anâ.. et â..inâ..), sauf sâ..il sont suivi par une
    # lettre a, e, i o, u ou un son 1 Ã  4 :
    r = re.sub(r'AN([^AEIOU1234])', r'1\1', r)
    r = re.sub(r'ON([^AEIOU1234])', r'1\1', r)
    r = re.sub(r'AM([^AEIOU1234])', r'1\1', r)
    r = re.sub(r'EN([^AEIOU1234])', r'1\1', r)
    r = re.sub(r'EM([^AEIOU1234])', r'1\1', r)
    r = re.sub(r'IN([^AEIOU1234])', r'4\1', r)

    # 9 remplacer les s par des z sâ..ils sont suivi et précédés des lettres a, e, i, o,u ou dâ..un son 1 Ã  4
    r = re.sub(r'([AEIOUY1234])S([AEIOUY1234])', r'\1Z\2', r)
    # CP : ajout du Y Ã  la liste

    # 10 remplacer les groupes de 2 lettres suivants :
    r = r.replace('OE', 'E')
    r = r.replace('EU', 'E')
    r = r.replace('AU', 'O')
    r = r.replace('OI', '2')
    r = r.replace('OY', '2')
    r = r.replace('OU', '3')

    # 11 remplacer les groupes de lettres suivants
    r = r.replace('CH', '5')
    r = r.replace('SCH', '5')
    r = r.replace('SH', '5')
    r = r.replace('SS', 'S')
    r = r.replace('SC', 'S')  # CP : problème pour PASCAL, mais pas pour PISCINE ?

    # 12 remplacer le c par un s s'il est suivi d'un e ou d'un i
    # CP : à mon avis, il faut inverser 11 et 12 et ne pas faire la dernière ligne du 11
    r = re.sub(r'C([EI])', r'S\1', r)

    # 13 remplacer les lettres ou groupe de lettres suivants :
    r = r.replace('C', 'K')
    r = r.replace('Q', 'K')
    r = r.replace('QU', 'K')
    r = r.replace('GU', 'K')
    r = r.replace('GA', 'KA')
    r = r.replace('GO', 'KO')
    r = r.replace('GY', 'KY')

    # 14 remplacer les lettres suivante :
    r = r.replace('A', 'O')
    r = r.replace('D', 'T')
    r = r.replace('P', 'T')
    r = r.replace('J', 'G')
    r = r.replace('B', 'F')
    r = r.replace('V', 'F')
    r = r.replace('M', 'N')

    # 15 Supprimer les lettres dupliquées
    oldc = '#'
    newr = ''
    for c in r:
        if oldc != c: newr = newr + c
        oldc = c
    r = newr

    # 16 Supprimer les terminaisons suivantes : t, x
    r = re.sub(r'(.*)[TX]$', r'\1', r)

    # 17 Affecter à chaque lettre le code numérique correspondant en partant de la dernière lettre
    num = ['1', '2', '3', '4', '5', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'N', 'O', 'R', 'S', 'T', 'U', 'W', 'X', 'Y', 'Z']
    l = []
    for c in r:
        l.append(num.index(c))

    # 18 Convertissez les codes numériques ainsi obtenu en un nombre de base 22 exprimé en virgule flottante.
    res = 0.
    i = 1
    for n in l:
        res = n * 22 ** -i + res
        i = i + 1

    return res