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
from scoreEtudiant import *

# extraction des données
def extract_mean_and_IC(path_to_folder, Z_alpha_sur_2 = 1.96):
    """
    on extrait toutes les données présentes dans le dossier path_to_folder
    IC: pour intervalle de confiance
    z_alpha sur 2 pour un intervalle de conf à 95%
    """
    # on récupère la liste des fichiers
    files = os.listdir(path_to_folder)

    # on extrait les données dans une variable pandas
    all_data = list()
    for file in files:
        with open(f"{path_to_folder}/{file}", "r") as f:
            temp = json.load(f)
            model = temp["model"]
            # et on supprimer temp["model"] pour ne pas l'afficher
            del temp["model"]
            temp = pd.DataFrame(temp)
            all_data.append(temp)
            if max(temp["modele_valide"]) >= 55:
                print(file, max(temp["modele_valide"]))
                print(model)
                print(folder)
                instance = load_instance("data/inst3")
                print(compute_score(instance, model))

    moyenne = sum(all_data) / len(all_data)
    variance = sum([(data - moyenne) ** 2 for data in all_data]) / len(all_data)
    ecart_type = np.sqrt(variance)
    ic = Z_alpha_sur_2 * ecart_type / np.sqrt(len(all_data))
    return moyenne, ic, all_data


# on liste les fichiers présents dans path_to_result
path_to_result = r"\\fysfile01\atomhome$\ma5706ba\Personal_Storage\cplt_sci\cplt_sci_metaheuristique\resultats\grid_on_inst2_iter_increased"
folders = os.listdir(path_to_result)

# affichage des courbes
fig = plt.figure()
fig.suptitle("Analyse des résultats de la simulation")

axs = fig.subplot_mosaic("""
                          1112
                          1113
                          1114
                          """)
for folder in folders:
    mean, ic, all_data = extract_mean_and_IC(path_to_result + "/" + folder)



    # courbe de la moyenne du score avec l'écart type
    axs['1'].plot(mean["score_kept"], label=folder)
    # for data in all_data:
    #     axs[0, 0].plot(data["score_kept"])
    axs['1'].fill_between(mean.index, mean["score_kept"] - ic["score_kept"], mean["score_kept"] + ic["score_kept"], alpha=0.2)
    axs['1'].set_title("Score moyen")
    axs['1'].legend()


    # courbe de la moyenne du "modele_valide" avec l'écart type
    axs['2'].plot(mean["modele_valide"])
    axs['2'].fill_between(mean.index, mean["modele_valide"] - ic["modele_valide"], mean["modele_valide"] + ic["modele_valide"], alpha=0.2)
    axs['2'].set_title("Modèle valide moyen")
    # for data in all_data:
    #     axs[0, 1].plot(data["modele_valide"])

    # courbe de la moyenne du "proba" avec l'écart type
    axs['3'].plot(mean["proba"])
    axs['3'].fill_between(mean.index, mean["proba"] - ic["proba"], mean["proba"] + ic["proba"], alpha=0.2)
    axs['3'].set_title("Proba")

    axs['4'].plot(mean["score_kept"]/max(mean["score_kept"]))
    axs['4'].set_title("Score normalisé")

# on show
plt.show()