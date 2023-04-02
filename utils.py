import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
# from relife import Weibull
pd.options.plotting.backend = "plotly"

class Dette:
    def __init__(self,montant,annee_debut,annee_fin):
        self.montant = montant
        self.annee_debut = annee_debut
        self.anne_fin = annee_fin
        self.duree = annee_fin - annee_debut
        if annee_fin > annee_debut:
            self.remboursement_annuel = montant/(annee_fin - annee_debut)
        else:
            self.remboursement_annuel = 0

class Capex:
    def __init__(self,montant,annee_debut,annee_fin,duree_amortissement):
        self.montant = montant
        self.annee_debut = annee_debut
        self.anne_fin = annee_fin
        self.duree = annee_fin - annee_debut
        if annee_fin > annee_debut:
            self.cout_annuel = montant/(annee_fin - annee_debut)
        else :
            self.cout_annuel = montant 
        self.duree_amortissement = duree_amortissement

class Opex:
    def __init__(self,montant,annee_debut,annee_fin):
        self.montant = montant
        self.annee_debut = annee_debut
        self.anne_fin = annee_fin
        self.duree = annee_fin - annee_debut

class Prix_MWh:
    def __init__(self,prix_MWh,annee_debut,annee_fin):
        self.prix_MWh = prix_MWh
        self.annee_debut = annee_debut
        self.anne_fin = annee_fin

class Production:
    def __init__(self,Nb_heures,capacite,annee_debut,annee_fin):
        self.Nb_heures = Nb_heures
        self.capacite = capacite
        self.production = capacite * Nb_heures
        self.annee_debut = annee_debut
        self.anne_fin = annee_fin