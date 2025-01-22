"""
le principe de ce fichier est de choisir automatiquement les meilleurs configurations pour la simulation
c'est une sorte d'amélioration du fichier simulation_principale (ou l'action humaine est nécessaire)
ici on va uniquementsauvegarder à la fin de chaque simulation sur une grid
le principe de l'algo est le suivant:
1/ on fixe aléatoirement un jeu de paramètres
2/ on fait une simulation pour chaque valeur de T_final et on garde le meilleur score (en terme de score_kept)
3/ on fait une simulation pour chaque valeur de T_init et on garde le meilleur score (en terme de score_kept)
4/ on fait une simulation pour chaque valeur de alpha et on garde le meilleur score (en terme de ville valide puis en terme de score_kept SANS pénalité)
5/ on fait une simulation pour chaque transformee et on garde le meilleur score (en terme de score_kept)
6/ on recommence à l'étape 2 jusqu'à ce que le jeu de paramètres reste inchangé pendant un tour complet
:auteur: Maxence BARRE
:date:2025
"""

# importations des modules
print("[INFO] Importation des modules")
import numpy as np
from scipy.stats import bernoulli
from scoreEtudiant import *
from annexe import *
import tqdm
import math as m
import time
from datetime import datetime
from annexe_fichier_principal import *
import os
print("[INFO] Modules importés")


###################################################################
# configuration de la simulation
grid_T_init = (10, 100, 500, 1000, 5000, 10000)
grid_T_final = (1, 0.1, 0.01, 0.001)
grid_alpha = (10, 100, 500, 1000, 5000, 10000)
grid_transformee = (transformee_pick_the_furthest, transformee_pick_among_non_valid, transformee_pick_2, transformee_pick_random)

all_the_grid = {"T_final": grid_T_final, "T_init": grid_T_init, "alpha": grid_alpha, "transformee": grid_transformee}
nb_iter = 10000
num_instance = "inst1"
path_to_instance = f"data/{num_instance}"

nb_simu = 10
###################################################################

# chargement de l'instance
# calcul de la matrice des distances du graphe
instance = load_instance(path_to_instance)
graphe_matrix = compute_dist_mat(instance)
print("Matrice des distances calculée")




# on initialise le jeu de paramètres
current_config = {
    "T_init": np.random.choice(grid_T_init),
    "T_final": np.random.choice(grid_T_final),
    "alpha": np.random.choice(grid_alpha),
    "transformee": np.random.choice(grid_transformee)
}

# initialisation des variables
# score_mean, valide_mean, score_without_punition_mean, time_axis_mean = mean_on_recuit_simule(T_init=current_config["T_init"], alpha=current_config["alpha"], nom=None, fonction_transformee=current_config["transformee"], T_final=current_config["T_final"], nb_iter=nb_iter, instance=instance, graphe_matrix=graphe_matrix, nb_simu=nb_simu)
nb_config_not_changed = 0       # a chaque fois que l'on ne trouve pas une meilleure config, on incrémente de 1
best_score = np.inf           # on initialise le meilleur score à l'infini (car on veut minimiser le score)
best_valide = 0
best_score_without_punition = np.inf
best_config = current_config.copy()    # on initialise le meilleur score avec la config actuelle

while nb_config_not_changed < 6:
    for cle_to_change in all_the_grid.keys():
        print("_________________________________________________________________________________________")
        print("[INFO] On fait varier le paramètre", cle_to_change)
        print("current best config : ", best_config)
        print("nb_config_not_changed : ", nb_config_not_changed)
        print("_________________________________________________________________________________________")
        has_changed = False
        current_config = best_config.copy()
        for value in all_the_grid[cle_to_change]:
            if value == current_config[cle_to_change]:
                continue
            print("[INFO] On change le paramètre", cle_to_change, "avec la valeur", value)
            current_config[cle_to_change] = value
            score_mean, valide_mean, score_without_punition_mean, time_axis_mean =mean_on_recuit_simule(T_init=current_config["T_init"], alpha=current_config["alpha"], nom=None, fonction_transformee=current_config["transformee"], T_final=current_config["T_final"], nb_iter=nb_iter, instance=instance, graphe_matrix=graphe_matrix, nb_simu=nb_simu)
            change_best_config = False
            if cle_to_change != "alpha" and score_mean < best_score:
                    change_best_config = True
            elif cle_to_change == "alpha" and (valide_mean >= best_valide):
                    if valide_mean == best_valide:
                        if score_without_punition_mean < best_score_without_punition:
                            change_best_config = True
                    else:
                        change_best_config = True
            if change_best_config:
                has_changed = True
                print("[INFO] Meilleur configuration trouvée en changeant:", cle_to_change, "avec la valeur", value)
                print(f"score : {score_mean}, valide : {valide_mean}, score_without_punition : {score_without_punition_mean}")
                best_score = score_mean
                best_valide = valide_mean
                best_score_without_punition = score_without_punition_mean
                best_config = current_config.copy()
                nb_config_not_changed = 0
        if has_changed:
            nb_config_not_changed = 0
        else:
            nb_config_not_changed += 1

print("[INFO] Meilleur configuration trouvée")
print(best_config)
print("done")