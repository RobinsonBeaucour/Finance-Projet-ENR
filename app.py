import streamlit as st
import pandas as pd
import numpy as np
import numpy_financial as npf
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from relife import Weibull
from utils import *
pd.options.plotting.backend = "plotly"

st.set_page_config(layout="wide",initial_sidebar_state="collapsed")

with st.sidebar:
    st.markdown(
    '''
    Cette application a un objectif pédagogique sur le financement d'un projet ENR (ou autre !).<br>
    Elle vise à placer l'utilisateur à la place d'un porteur de projet. 
    ''',unsafe_allow_html=True
    )
    with st.expander("Définitions",expanded=False):
        st.markdown(
        '''
        <u>CAPEX</u>: Dépense d'investissement, ce type de dépense peut engendrer des baisses d'impôts (<i>via</i> les amortissements) ou des revenus (dans un model RAB / Base d'actifs régulés)<br>
        <u>OPEX</u> : Dépense d'exploitation, dans cette application les OPEX regroupent toutes les dépenses autres que CAPEX, impôts, frais financiers. <br>
        <u>Amortissements</u> : L'amortissement comptable d'un investissement pour une entreprise est l'étalement de son coût sur sa durée d'utilisation. Il s'agit d'un flux compable pris en compte dans le calcul des impôts de l'investisseur.
        ''',unsafe_allow_html=True
        )
    st.markdown(
    '''
    ## Valeur actualisée nette 
    '''
    )
    st.markdown(
    '''
    La <u>valeur actualisée nette</u> pour un taux d'actualisation (r) fixé donne la mesure de rentabilité d'un projet. Elle se définit par l'équation ci-dessous.
    ''',unsafe_allow_html=True
    )
    st.latex(
        r'''
        VAN(r) = \sum_{t=n_{0}}^{N} \frac{CF_t}{(1+r)^t} =\sum_{t=n_{0}}^{N} \frac{Recette_t-Dépense_t}{(1+r)^t}
        '''
    )
    st.markdown(
        '''
        $CF_t$ indique le cash flow du projet pendant l'année $t$
        '''
    )
    st.markdown(
    '''
    Le <u>taux de rendement interne</u> est le taux d'actualisation (r) qui annule la valeur actualisée nette.<br>
    ''',unsafe_allow_html=True
    )
    st.markdown(
    '''
    Le <u>Levelized cost of electricity</u> pour un taux d'actualisation (r) peut s'interpréter comme le prix de vente de l'électricité qui annule la VAN avec le taux r.
    ''',unsafe_allow_html=True
    )
    st.latex(
        r'''
        LCOE(r) = \sum_{t=n_{0}}^{N} \frac{Recette_t-Dépense_t}{(1+r)^t}
        '''
    )

row0_spacer1, row0_1, row0_2, row0_spacer3 = st.columns((.1, 1.5, 1.0, .1))
with row0_1:
    st.title("Financement d'un projet de production d'énergie")
with row0_2:
    st.text("")
 #   st.subheader('Streamlit App réalisée par [Robinson Beaucour](https://www.linkedin.com/in/robinson-beaucour-a81403177)')
    st.markdown("<h3 style='text-align: right'>Streamlit App réalisée par<br> <a href='https://www.linkedin.com/in/robinson-beaucour-a81403177'>Robinson Beaucour</a></h3>", unsafe_allow_html=True)

st.markdown("## Durée du projet")
cols = st.columns(6)
with cols[1]:
    annee_debut_projet = st.number_input(
        "Année de début",
        step = 1, 
        value = -2,
        help = "Année de début du projet",
        # label_visibility="collapsed"
        )
    
with cols[2]:
    annee_fin_projet = st.number_input(
        "Année de fin",
        step = 1, 
        value = 30,
        help = "Année de fin du projet",
        # label_visibility="collapsed"
        )
    
with cols[3]:
    taux_imposition = 1/100* st.number_input("Taux d'imposition", min_value=0, max_value=100,step =1, value = 25, help = "Taux d'imposition sur les société (en %)")
    
with cols[4]:
    taux_interets = 1/100* st.number_input("Taux d'intérêt", min_value=-5, max_value=25,step =1, value = 3, help = "Taux d'intérêt des prêts (en %)")

cols = st.columns(5)

with cols[0]:
    st.markdown("### CAPEX")
    Nb_period_CAPEX = st.number_input(
        "Nombre de période",
        step = 1,
        value = 1,
        min_value = 0,
        help = "Nombre de période où des CAPEX sont présents dans le projet"
    )
    list_capex = []
    for k in range(1,Nb_period_CAPEX+1):
        with st.expander(f"CAPEX {k}",False):
            list_capex.append(
                Capex(
                montant = -float(st.text_input(
                "Montant",
                value = "100000000",
                help = "Montant du CAPEX sur l'ensemble de la période",
                key = f"montant capex {k}"
                )),
                annee_debut=float(st.number_input(
                "Début",
                min_value = annee_debut_projet,
                max_value = annee_fin_projet,
                step = 1,
                help = "Année projet du début de l'engagement des CAPEX (doit être compris entre l'année de début et de fin du projet)",
                key = f"debut capex {k}"
                )),
                annee_fin=float(st.number_input(
                "Fin",
                min_value = annee_debut_projet,
                max_value = annee_fin_projet,
                step = 1,
                help = "Année projet de la fin de l'engagement des CAPEX (doit être compris entre l'année de début et de fin du projet)",
                key = f"fin capex {k}"
                )),
                duree_amortissement = float(st.number_input(
                "Durée d'amortissement",
                min_value=1,
                step = 1,
                help = "Durée d'amortissement comptable",
                key = f"amortissement capex {k}"
                ))
                )
                )

with cols[1]:
    st.markdown("### OPEX")
    Nb_period_OPEX = st.number_input(
        "Nombre de période",
        step = 1,
        value = 1,
        min_value = 0,
        help = "Nombre de période où des OPEX sont présents dans le projet"
    )
    list_opex = []
    for k in range(1,Nb_period_OPEX+1):
        with st.expander(f"OPEX {k}",False):
            list_opex.append(
                Opex(
                montant= -float(st.text_input(
                "Montant",
                value="300000",
                help = "Coût annuel en OPEX sur la période",
                key = f"montant opex {k}"
                )),
                annee_debut=st.number_input(
                "Début",
                min_value=annee_debut_projet,
                max_value=annee_fin_projet,
                value = 1,
                help = "Année projet de début des OPEX (doit être compris entre l'année de début et de fin du projet)",
                key =f"debut opex {k}"
                ),
                annee_fin=st.number_input(
                "Fin",
                min_value=annee_debut_projet,
                max_value=annee_fin_projet,
                value = annee_fin_projet,
                help = "Année projet de fin des OPEX (doit être compris entre l'année de début et de fin du projet)",
                key = f"fin opex {k}"
                ),
                )
            )

with cols[2]:
    st.markdown("### Production")
    Nb_period_prod = st.number_input(
        "Nombre de période",
        step = 1,
        value = 1,
        min_value = 0,
        help = "Nombre de période de production énergétique dans le projet"
    )
    list_prod = []
    for k in range(1,Nb_period_prod+1):
        with st.expander(f"Production {k}",False):
            list_prod.append(
                Production(
                Nb_heures=st.number_input(
                "Nombre d'heures à puissance nomnale",
                min_value=0,
                max_value=8760,
                step=100,
                value = 2200,
                help="Nombre d'heures annuelles d'équivalent puissance nominale sur la période",
                key=f"heure {k}"
                ),
                capacite=st.number_input(
                "Capacité (MW)",
                min_value = 0,
                max_value = 2000,
                step = 10,
                value = 100,
                help = "Capacité de production en MW sur la période",
                key = f"capacite {k}"
                ),
                annee_debut=st.number_input(
                    "Début",
                    min_value=annee_debut_projet,
                    max_value=annee_fin_projet,
                    value = 1,
                    help = "Année projet de début de la production (doit être compris entre l'année de début et de fin du projet)",
                    key =f"debut prod {k}"
                    ),
                annee_fin=st.number_input(
                    "Fin",
                    min_value=annee_debut_projet,
                    max_value=annee_fin_projet,
                    value = annee_fin_projet,
                    help = "Année projet de fin de la production (doit être compris entre l'année de début et de fin du projet)",
                    key =f"fin prod {k}"
                    ),
                )
            )

with cols[3]:
    st.markdown("### Prix de vente")
    Nb_period_vente = st.number_input(
        "Nombre de période",
        step = 1,
        value = 1,
        min_value = 0,
        help = "Nombre de période de prix de l'énergie dans le projet"
    )
    list_prix_MWh = []
    for k in range(1,Nb_period_vente+1):
        with st.expander(f"Prix de vente {k}",False):
            list_prix_MWh.append(
                Prix_MWh(
                prix_MWh=st.number_input(
                "Prix de vente (€/MWh)",
                min_value = 0.0,
                max_value = 450.0,
                value = 70.0,
                step = 0.5,
                help = "Prix de vente du MWh sur la période",
                key = f"prix {k}"
                ),
                annee_debut= st.number_input(
                "Début",
                min_value=annee_debut_projet,
                max_value=annee_fin_projet,
                value = 1,
                help = "Année projet de début du prix de vente (doit être compris entre l'année de début et de fin du projet)",
                key =f"debut prix {k}"
                ),
                annee_fin= st.number_input(
                "Fin",
                min_value=annee_debut_projet,
                max_value=annee_fin_projet,
                value = annee_fin_projet,
                help = "Année projet de fin du prix de vente (doit être compris entre l'année de début et de fin du projet)",
                key =f"fin prix {k}"
                )
                )
            )

with cols[4]:
    st.markdown("### Dette")
    Nb_period_dette = st.number_input(
        "Nombre de période",
        step = 1,
        value = 1,
        min_value = 0,
        help = "Nombre d'emprunts dans le projet"
    )
    list_dette = []
    for k in range(1,Nb_period_dette+1):
        with st.expander(f"Dette {k}",False):
            list_dette.append(
                Dette(
                montant = float(st.text_input(
                "Montant",
                "400000",
                help = "Montant de la dette (en €)",
                key = f"dette {k}"
                )),
                annee_debut= st.number_input(
                "Début",
                min_value=annee_debut_projet,
                max_value=annee_fin_projet,
                value = annee_debut_projet,
                help = "Année projet de début de l'emprunt (doit être compris entre l'année de début et de fin du projet)",
                key =f"debut dette {k}"
                ),
                annee_fin= st.number_input(
                "Fin",
                min_value=annee_debut_projet,
                max_value=annee_fin_projet,
                value = 1,
                help = "Année projet de fin de l'emprunt (doit être compris entre l'année de début et de fin du projet)",
                key =f"fin dette {k}"
                )
                )
            )

df = pd.DataFrame(columns=[k for k in range(annee_debut_projet,annee_fin_projet+1)])
df.loc["Coef. actualisation"] = [(1+1/100)**k for k in df.columns]

df.loc["CAPEX"] = 0
for capex in list_capex:
    df.loc["CAPEX",capex.annee_debut:capex.anne_fin] += capex.cout_annuel

df.loc["OPEX"] = 0
for opex in list_opex:
    df.loc["OPEX",opex.annee_debut:opex.anne_fin] += opex.montant

df.loc["Prod. (MWh)"] = 0
for prod in list_prod:
    df.loc["Prod. (MWh)",prod.annee_debut:prod.anne_fin] = prod.production

df.loc["Revenus"] = 0
for prix_MWh in list_prix_MWh:
    df.loc["Revenus",prix_MWh.annee_debut:prix_MWh.anne_fin] += prix_MWh.prix_MWh * df.loc["Prod. (MWh)",prix_MWh.annee_debut:prix_MWh.anne_fin]

df.loc["EBITDA"] = df.loc[["OPEX","Revenus"]].sum()

df.loc["Amortissements"] = 0
for capex in list_capex:
    df.loc["Amortissements",capex.anne_fin+1:capex.anne_fin+capex.duree_amortissement] += capex.montant/capex.duree_amortissement
df.loc["EBIT"] = df.loc[["EBITDA","Amortissements"]].sum()

df.loc["Dette BOP"] = 0
df.loc["Tirage"]    = 0
df.loc["Dette EOP"] = 0
df.loc["Remboursement"] = 0
df.loc["Intérêts financiers"] = 0

for dette in list_dette:
    df.loc["Dette BOP",dette.annee_debut:dette.anne_fin-1] += [dette.remboursement_annuel * (dette.duree - k) for k in range(dette.duree)]
    df.loc["Tirage",dette.annee_debut] += dette.montant
    df.loc["Remboursement",dette.annee_debut:dette.anne_fin-1] += - dette.remboursement_annuel
    df.loc["Dette EOP"] = df.loc[["Dette BOP", "Remboursement"]].sum()
    df.loc["Intérêts financiers"] += - df.loc["Dette BOP"] * taux_interets

df.loc["Résultat avant IS"] = df.loc[["EBIT","Intérêts financiers","Remboursement"]].sum()
df.loc["Impôts (IS)"] = - df.loc["Résultat avant IS"].apply(lambda x : 0 if x < 0 else x) * taux_imposition
df.loc["Résultat net"] = df.loc[["Résultat avant IS","Impôts (IS)"]].sum()
df.loc["Cash Flow"] = df.loc[["OPEX","CAPEX","Revenus","Intérêts financiers", "Impôts (IS)","Tirage","Remboursement"]].sum()
df.loc["DSCR"] = -df.loc[["EBITDA","Impôts (IS)"]].sum()/df.loc[["Intérêts financiers","Remboursement"]].sum()

fig = go.Figure()
list_to_show = ["CAPEX","OPEX","Revenus","Impôts (IS)","Tirage","Remboursement","Intérêts financiers"]
for flux in list_to_show:
    fig.add_trace(
        go.Bar(
        x = df.columns,
        y = df.loc[flux],
        name = flux
        )
    )

fig.add_trace(
    go.Scatter(
        x = df.columns,
        y = df.loc["Cash Flow"],
        name = "Cash Flow",
        marker_color = "black"
    )
)
fig.add_trace(
    go.Scatter(
        x = df.columns,
        y = df.loc["Dette BOP"],
        name = "Endettement",
        marker_color = "orange"
    )
)
fig.update_layout(
    hovermode = 'x',
    barmode = "relative",
    title = f"Flux financiers du projet - TRI : {np.round(npf.irr(df.loc['Cash Flow'])*100,2)} %",
    xaxis_title = "Valeur (€)",
    yaxis_title = "Année du projet",
    height = 600
)

st.plotly_chart(fig,use_container_width=True)

with st.expander("Tableau bilan",False):
    st.dataframe(df,use_container_width=True)

col1, col2, col3, col4 = st.columns([1,1,2,6])
with col2:
    taux_actualisation = st.number_input(
        "Taux d'actualisation",
        value = 7.0,
        min_value= -5.0,
        max_value=25.0,
        step = 0.5,
        help = "Taux d'actualisation pour le calcul des valeurs actualisées nettes (%)"
    )
    df.loc["Coef. actualisation"] = [(1+taux_actualisation/100)**k for k in df.columns]
with col3:
    st.markdown(f"### TRI : {np.round(npf.irr(df.loc['Cash Flow'])*100,2)} %")
dd = df / df.loc["Coef. actualisation"]

def groupement_année(k):
    if k<=0:
        return "Années négatives"
    else:
        return f"Années {((k-1)//5)*5+1}-{((k-1)//5+1)*5}"
de = pd.melt(dd.loc[["OPEX","CAPEX","Revenus","Impôts (IS)","Tirage","Remboursement","Intérêts financiers"]].reset_index(),id_vars="index").rename({"variable":"Année projet","index":"Type de flux"},axis=1)

def positif_negatif(k):
    if k>= 0:
        return "Positif"
    if k < 0:
        return "Négatif"
de["Sens"] = de["value"].apply(positif_negatif)
de["value"] = de["value"].abs().round()
de["Période projet"] = de["Année projet"].apply(groupement_année)

col1, col2 = st.columns([70,30])

with col1:
    fig = px.treemap(
        de, 
        path = [px.Constant("Ensemble du projet"), "Sens","Type de flux", "Période projet", "Année projet"], 
        values="value",
        # color = "Type de flux",
        maxdepth=3
    )
    fig.data[0].textinfo = 'label+value'
    fig.update_traces(root_color="lightgrey")
    fig.update_layout(
        title = "Valeur actualisée des flux du projet",
        height = 600
        )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    aa = pd.DataFrame(dd.loc[["CAPEX","OPEX","Revenus","Impôts (IS)","Tirage","Remboursement","Intérêts financiers"]].sum(1),columns=["Initial"])
    aa["Positif"] = dd.sum(1).apply(lambda x : 0 if x < 0 else x)
    aa["Négatif"] = -dd.sum(1).apply(lambda x : 0 if x > 0 else x)
    fig = go.Figure()
    for flux in list_to_show:
        fig.add_trace(
            go.Bar(
            x = aa[["Positif","Négatif"]].columns,
            y = aa[["Positif","Négatif"]].loc[flux],
            name = flux
            )
        )

        fig.update_layout(
        barmode = "relative",
        title = "Valeur actualisée nette des flux financiers du projet",
        xaxis_title = "Valeur (€)",
        height = 600
        )
    st.plotly_chart(fig,use_container_width=True)

fig = go.Figure()
list_to_show = ["CAPEX","OPEX","Revenus","Impôts (IS)","Tirage","Remboursement","Intérêts financiers"]
for flux in list_to_show:
    fig.add_trace(
        go.Bar(
        x = dd.columns,
        y = dd.loc[flux],
        name = flux
        )
    )

fig.add_trace(
    go.Scatter(
        x = dd.columns,
        y = dd.loc["Cash Flow"],
        name = "Cash Flow",
        marker_color = "black"
    )
)
fig.add_trace(
    go.Scatter(
        x = dd.columns,
        y = dd.loc["Dette BOP"],
        name = "Endettement",
        marker_color = "orange"
    )
)
fig.update_layout(
    hovermode = 'x',
    barmode = "relative",
    title = f"Flux financiers du projet - Taux d'actualisation : {taux_actualisation} %",
    xaxis_title = "Valeur (€)",
    yaxis_title = "Année du projet",
    height = 600
)

st.plotly_chart(fig,use_container_width=True)