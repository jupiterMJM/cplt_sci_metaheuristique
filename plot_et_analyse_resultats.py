"""
ce fichier permet d'analyser graphiquement les résultats de la simulation
la méthode est la suivante:
- on charge les données de la simulation
- on calcul la moyenne et l'écart type de chaque variable
- on affiche les courbes de chaque variable
l'affichage des courbes sera faite grâce à matplotlib : 4 graphiques différents dans une même fenêtre
"""

# importation des modules
import json
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd

# extraction des données
def extract_mean_and_variance(path_to_folder):
    """
    on extrait toutes les données présentes dans le dossier path_to_folder
    """
    # on récupère la liste des fichiers
    files = os.listdir(path_to_folder)

    # on extrait les données dans une variable pandas
    all_data = list()
    for file in files:
        with open(f"{path_to_folder}/{file}", "r") as f:
            temp = json.load(f)
            temp = pd.DataFrame(temp)
            all_data.append(temp)

    moyenne = sum(all_data) / len(all_data)
    variance = sum([(data - moyenne) ** 2 for data in all_data]) / len(all_data)
    ecart_type = np.sqrt(variance)
    return moyenne, ecart_type, all_data


mean, variance, all_data = extract_mean_and_variance("resultats/inst1_10_0.9999_1000")

# affichage des courbes
fig, axs = plt.subplots(2, 2)
fig.suptitle("Analyse des résultats de la simulation")

# courbe de la moyenne du score avec l'écart type
axs[0, 0].plot(mean["score_kept"])
# for data in all_data:
#     axs[0, 0].plot(data["score_kept"])
axs[0, 0].fill_between(mean.index, mean["score_kept"] - variance["score_kept"], mean["score_kept"] + variance["score_kept"], alpha=0.2)
axs[0, 0].set_title("Score moyen")


# courbe de la moyenne du "modele_valide" avec l'écart type
axs[0, 1].plot(mean["modele_valide"])
axs[0, 1].fill_between(mean.index, mean["modele_valide"] - variance["modele_valide"], mean["modele_valide"] + variance["modele_valide"], alpha=0.2)
axs[0, 1].set_title("Modèle valide moyen")
# for data in all_data:
#     axs[0, 1].plot(data["modele_valide"])

# courbe de la moyenne du "proba" avec l'écart type
axs[1, 0].plot(mean["proba"])
axs[1, 0].fill_between(mean.index, mean["proba"] - variance["proba"], mean["proba"] + variance["proba"], alpha=0.2)
axs[1, 0].set_title("Proba")

# on show
plt.show()