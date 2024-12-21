"""
fichier annexe pour la résolution du problème de voyageur de commerce avec fenètre de temps
:auteur: Maxence BARRE
"""

import random

def transformee_pick_2(liste_ville):
    """
    sélectionne aléatoirement deux villes dans la liste des villes et les échange
    """
    temp = liste_ville.copy()
    i, j =random.sample(list(range(1, len(liste_ville))), 2)
    temp[i], temp[j] = temp[j], temp[i]
    return temp


def transformee_pick_random(liste_ville):
    """
    sélectionne aléatoirement un nombre aléatoire de villes dans la liste des villes et les échange
    """
    n = random.randint(2, len(liste_ville)-1)
    indic =random.sample(list(range(1, len(liste_ville))), n)
    new_indic = random.sample(indic, len(indic))
    for i in range(n):
        liste_ville[indic[i]], liste_ville[new_indic[i]] = liste_ville[new_indic[i]], liste_ville[indic[i]]
    
    return liste_ville


def find_ville_non_valide(liste_ville, instance, graphe_matrix):
    time_axis = 0
    ville_non_valide = []
    for i, prop in enumerate(liste_ville):
        if i == 0: continue
        # on commence par aller jusqu'à la ville i
        time_axis += graphe_matrix[int(liste_ville[i-1])][int(liste_ville[i])]

        # si on est arrivé trop tôt, on attend
        if time_axis < instance[prop]["wstart"]:
            time_axis = instance[prop]["wstart"]

        
        if time_axis > instance[prop]["wend"]:
            ville_non_valide.append(prop)

    return ville_non_valide

def transformee_pick_among_non_valid(liste_ville, instance, graphe_matrix):
    """
    sélectionne aléatoire deux villes non valide et la remplace par une autre ville aléatoirement
    """
    temp = liste_ville.copy()
    ville_non_valide = find_ville_non_valide(liste_ville, instance, graphe_matrix)
    if len(ville_non_valide) == 0: # il n'y a plus de villes non valides
        return transformee_pick_2(liste_ville)
    else:
        ville1 = random.choice(ville_non_valide)
        ville2 = random.choice(liste_ville)
        # print(ville2, type(ville2))
        while ville2 == ville1 or ville2 == "1":
            ville2 = random.choice(liste_ville)
        
        i = liste_ville.index(ville1)
        j = liste_ville.index(ville2)
        temp[i], temp[j] = temp[j], temp[i]
        return temp