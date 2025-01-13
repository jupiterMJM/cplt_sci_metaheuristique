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
print("[INFO] Modules importés")

###################################################################
# configuration de la simulation
# configuration
T_init = 10
lbd = 0.9999
nb_iter = 50000
path_to_instance = "data/inst1"
alpha = 50

def f(temp):
    # if iter % 10000 == 0:
    #     return T_init / (iter // 10000 +1)
    return temp * lbd

# on met la date et l'heure de la simu
nom = f"simu_{T_init}_{lbd}_{alpha}_on_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
###################################################################


# chargement de l'instance
# calcul de la matrice des distances du graphe
instance = load_instance(path_to_instance)
graphe_matrix = compute_dist_mat(instance)
print("Matrice des distances calculée")


for i in range(10):
    print(f"itération {i+1}")
    # on lance la simulation
    historique = recuit_simule(T_init, alpha, nom, transformee_pick_2, f, nb_iter, instance, graphe_matrix)
    print("sauvegarde des données")
    historique.save(f"resultats/{nom}_{i}.json")
    print("fin de l'itération")