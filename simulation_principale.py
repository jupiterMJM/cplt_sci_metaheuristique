"""
l'objectif de ce fichier est de reprendre exactement le principe de brouillon.ipynb 
en le remettant en forme dans un fichier "plus propre"
:auteur: Maxence BARRE
:date: 2025
:note: ce programme n'affichera pas les résultats, pour les plot il faudra lancer un autre fichier
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
# configuration
T_final = 0.1
nb_iter = 10000
num_instance = "inst1"
transformee = transformee_pick_the_furthest
path_to_instance = f"data/{num_instance}"
alpha = 1000

def f(temp):
    # if iter % 10000 == 0:
    #     return T_init / (iter // 10000 +1)
    return temp * lbd

# # on met la date et l'heure de la simu
# nom_folder = f"{num_instance}_{transformee.__name__}_{T_init}_{lbd}_{alpha}"
nb_simu = 30
###################################################################


# chargement de l'instance
# calcul de la matrice des distances du graphe
instance = load_instance(path_to_instance)
graphe_matrix = compute_dist_mat(instance)
print("Matrice des distances calculée")


# on regarde si le dossier nom_folder existe
# s'il existe on lève une erreur
# sinon on le créé
# if os.path.exists(f"resultats/{nom_folder}"):
#     raise ValueError("le dossier existe déjà, veuillez changer le nom de la simulation")
# else:
#     os.mkdir(f"resultats/{nom_folder}")

for T_init in  (5, 10, 20, 50, 100, 500, 1000):
    lbd = np.exp(np.log(T_final/T_init)/nb_iter)
    print("[INFO] Simulation avec T_init = ", T_init, " et lbd = ", lbd)
    # on met la date et l'heure de la simu
    nom_folder = f"{num_instance}_{transformee.__name__}_{T_init}_{lbd}_{alpha}"
    if os.path.exists(f"resultats/{nom_folder}"):
        raise ValueError("le dossier existe déjà, veuillez changer le nom de la simulation")
    else:
        os.mkdir(f"resultats/{nom_folder}")
    for i in range(nb_simu):
        print(f"itération {i+1}")
        # on lance la simulation
        historique = recuit_simule(T_init, alpha, nom_folder, transformee, f, nb_iter, instance, graphe_matrix)
        print("sauvegarde des données")
        historique.save(f"resultats/{nom_folder}/simu_{i}.json")
        print("fin de l'itération")