"""
fichier annexe pour la résolution du problème de voyageur de commerce avec fenètre de temps
:auteur: Maxence BARRE
"""

import random

def transformee_pick_2(liste_ville):
    """
    sélectionne aléatoirement deux villes dans la liste des villes et les échange
    """
    i, j =random.sample(list(range(1, len(liste_ville))), 2)
    liste_ville[i], liste_ville[j] = liste_ville[j], liste_ville[i]
    return liste_ville