"""
fichier annexe pour la résolution du problème de voyageur de commerce avec fenètre de temps
:auteur: Maxence BARRE
"""

import random

def transformee_pick_2(liste_ville, *args):
    """
    sélectionne aléatoirement deux villes dans la liste des villes et les échange
    """
    temp = liste_ville.copy()
    i, j =random.sample(list(range(1, len(liste_ville))), 2)
    temp[i], temp[j] = temp[j], temp[i]
    return temp


def transformee_pick_random(liste_ville, *args):
    """
    sélectionne aléatoirement un nombre aléatoire de villes dans la liste des villes et les échange
    """
    temp = liste_ville.copy()
    n = random.randint(2, len(liste_ville)-1)
    indic =random.sample(list(range(1, len(liste_ville))), n)
    new_indic = random.sample(indic, len(indic))
    for i in range(n):
        temp[indic[i]], temp[new_indic[i]] = temp[new_indic[i]], temp[indic[i]]
    
    return temp


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
    

def transformee_pick_the_furthest(liste_ville, instance, graphe_matrix):
    """
    sélectionne la ville la plus éloignée et la remplace par une autre ville aléatoirement
    """
    temp = liste_ville.copy()
    ville1 = liste_ville[1] # car on ne prend pas la ville de départ (1)
    dist_ville1 = graphe_matrix[int("1")][int(ville1)]
    for i, ville in enumerate(liste_ville):
        if i <= 1:
            continue
        if graphe_matrix[int(liste_ville[i-1])][int(ville)] > dist_ville1:
            ville1 = ville
            dist_ville1 = graphe_matrix[int(liste_ville[i-1])][int(ville)]
    ville2 = random.choice(liste_ville)
    while ville2 == ville1 or ville2 == "1":
        ville2 = random.choice(liste_ville)
    
    i = liste_ville.index(ville1)
    j = liste_ville.index(ville2)
    temp[i], temp[j] = temp[j], temp[i]
    return temp