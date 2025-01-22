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
        self.score_without_punition = []
        self.modele_valide = []
        self.time_axis = []
        self.score_kept = []
        self.i = 0  # on ne veut pas garder toutes les données, uniquement 1 sur 5
        self.model = None

    def append(self, temperature, proba, score, score_without_punition, valide_kept, time_axis, score_kept):
        self.i += 1
        if self.i % 5 == 0:
            # self.temperature.append(temperature)
            self.proba.append(proba)
            # self.score.append(score)
            self.score_without_punition.append(score_without_punition)
            self.modele_valide.append(valide_kept)
            self.time_axis.append(time_axis)
            self.score_kept.append(score_kept)

    def keep_model(self, model):
        self.model = model

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
            "score_kept": self.score_kept,
            "model": self.model
        }
        with open(path, "w") as f:
            json.dump(data, f)


def recuit_simule(T_init, alpha, nom, fonction_transformee, evol_temp, nb_iter, instance, graphe_matrix, build_historique=True, taqadum=True):
    """
    fonction principale de la simulation
    reprend l'entièreté de la simulation présente dans le fichier brouillon.ipynb
    """
    # initialisation de l'algorithme
    modele = list(instance.keys())
    modele = ["1"] + rd.sample(modele[1:], len(modele)-1)
    # print(modele)
    temperature = T_init
    proba = 1
    modele_kept = modele.copy()
    score_kept, valide_kept, score_without_punition_kept,  time_axis = evaluation_model(modele_kept, alpha, instance, graphe_matrix)
    if build_historique: historique = Historique()

    if taqadum:
        iterate_on_it = tqdm(range(nb_iter))
    else:
        iterate_on_it = range(nb_iter)
    for iteration in iterate_on_it:
        # on commence par appliquer une transformation aléatoire
        modele = fonction_transformee(modele_kept, instance, graphe_matrix)# , instance=instance, graphe_matrix=graphe_matrix)

        # on détermine le score du modèle ainsi modifié
        score, valide, score_without_punition, time_axis = evaluation_model(modele, alpha, instance, graphe_matrix)

        # on accepte ou non la modification (recuit simulé)
        if score <= score_kept:
            modele_kept = modele.copy()
            score_kept = score
            valide_kept = valide
            score_without_punition_kept = score_without_punition
        else:   # alors score >= score_kept
            # la proba est calculée ici pour des soucis de cohérences avec les historiques
            proba = np.exp(-(score-score_kept)/temperature)
            # if proba == 1: print(score, score_kept, temperature)
            if bernoulli.rvs(proba, size=1):    # variable de bernoulli
                modele_kept = modele.copy()
                score_kept = score
                valide_kept = valide
                score_without_punition_kept = score_without_punition

        # on enregistre les données
        if build_historique: historique.append(temperature=temperature, proba=proba, score=score, score_without_punition=score_without_punition, valide_kept=valide_kept, time_axis=time_axis, score_kept=score_kept)

        # on met à jour la température puis ça repart
        temperature = evol_temp(temperature)
    if build_historique:
        historique.keep_model(modele_kept)
        return historique
    else:
        return score_kept, valide_kept, score_without_punition_kept, time_axis
    


def mean_on_recuit_simule(T_init, alpha, nom, fonction_transformee, T_final, nb_iter, instance, graphe_matrix, nb_simu):
    """
    on fait une moyenne sur plusieurs simulations
    """
    all_score = list()
    all_valide = list()
    all_score_without_punition = list()
    all_time_axis = list()
    for i in range(nb_simu):
        # print("simulation", i+1)
        lbd = np.exp(np.log(T_final/T_init)/nb_iter)
        evol_temp = lambda temp: lbd*temp
        score, valide, score_without_punition, time_axis = recuit_simule(T_init, alpha, nom, fonction_transformee, evol_temp, nb_iter, instance, graphe_matrix, build_historique=False, taqadum=False)
        all_score.append(score)
        all_valide.append(valide)
        all_score_without_punition.append(score_without_punition)
        all_time_axis.append(time_axis)
    return np.mean(all_score), np.mean(all_valide), np.mean(all_score_without_punition), np.mean(all_time_axis)