import json
import random as rd
from tqdm import tqdm
from scipy.stats import bernoulli
import numpy as np

def evaluation_model(liste_prop, alpha, instance, graphe_matrix):
    """
    évalue le modèle en fonction de la liste des propositions
    la formule choisie est la somme des distances plus une pénalité binaire pour chaque consigne de temps non respectée
    :rq: on utilise les variables globales instance et graphe_matrix
    """
    score = 0
    score_without_punition = 0
    assert liste_prop[0] == "1", "La première ville n'est pas 1 : {}".format(liste_prop)
    time_axis = 0
    valide = len(liste_prop)
    for i, prop in enumerate(liste_prop):
        if i == 0: continue
        # on commence par aller jusqu'à la ville i
        time_axis += graphe_matrix[int(liste_prop[i-1])][int(liste_prop[i])]

        # si on est arrivé trop tôt, on attend
        if time_axis < instance[prop]["wstart"]:
            time_axis = instance[prop]["wstart"]

        # on ajoute le cout au score
        score += graphe_matrix[int(liste_prop[i-1])][int(prop)]
        score_without_punition += graphe_matrix[int(liste_prop[i-1])][int(prop)]

        # on ajoute une pénalité si on arrive trop tard (consigne de temps non respectée)
        if time_axis > instance[prop]["wend"]:
            score += alpha
            valide -= 1
    
    return score, valide, score_without_punition, time_axis


class Historique:
    def __init__(self):
        # self.temperature = []
        self.proba = []
        # self.score = []
        # self.score_without_punition = []
        self.modele_valide = []
        self.time_axis = []
        self.score_kept = []
        self.i = 0  # on ne veut pas garder toutes les données, uniquement 1 sur 5

    def append(self, temperature, proba, score, score_without_punition, valide_kept, time_axis, score_kept):
        self.i += 1
        if self.i % 5 == 0:
            # self.temperature.append(temperature)
            self.proba.append(proba)
            # self.score.append(score)
            # self.score_without_punition.append(score_without_punition)
            self.modele_valide.append(valide_kept)
            self.time_axis.append(time_axis)
            self.score_kept.append(score_kept)

    def save(self, path):
        """
        on enregistre les données au format json
        """
        data = {
            # "temperature": self.temperature,
            "proba": self.proba,
            # "score": self.score,
            # "score_without_punition": self.score_without_punition,
            "modele_valide": self.modele_valide,
            "time_axis": self.time_axis,
            "score_kept": self.score_kept
        }
        with open(path, "w") as f:
            json.dump(data, f)


def recuit_simule(T_init, alpha, nom, fonction_transformee, evol_temp, nb_iter, instance, graphe_matrix):
    """
    fonction principale de la simulation
    reprend l'entièreté de la simulation présente dans le fichier brouillon.ipynb
    """
    # initialisation de l'algorithme
    modele = list(instance.keys())
    modele = ["1"] + rd.sample(modele[1:], len(modele)-1)
    print(modele)
    temperature = T_init
    proba = 1
    modele_kept = modele.copy()
    score_kept, valide_kept, score_without_punition,  time_axis = evaluation_model(modele_kept, alpha, instance, graphe_matrix)
    historique = Historique()

    for iteration in tqdm(range(nb_iter)):
        # on commence par appliquer une transformation aléatoire
        modele = fonction_transformee(modele_kept, instance, graphe_matrix)# , instance=instance, graphe_matrix=graphe_matrix)

        # on détermine le score du modèle ainsi modifié
        score, valide, score_without_punition, time_axis = evaluation_model(modele, alpha, instance, graphe_matrix)

        # on accepte ou non la modification (recuit simulé)
        if score <= score_kept:
            modele_kept = modele.copy()
            score_kept = score
            valide_kept = valide
        else:   # alors score >= score_kept
            # la proba est calculée ici pour des soucis de cohérences avec les historiques
            proba = np.exp(-(score-score_kept)/temperature)
            # if proba == 1: print(score, score_kept, temperature)
            if bernoulli.rvs(proba, size=1):    # variable de bernoulli
                modele_kept = modele.copy()
                score_kept = score
                valide_kept = valide

        # on enregistre les données
        historique.append(temperature=temperature, proba=proba, score=score, score_without_punition=score_without_punition, valide_kept=valide_kept, time_axis=time_axis, score_kept=score_kept)

        # on met à jour la température puis ça repart
        temperature = evol_temp(temperature)
    return historique