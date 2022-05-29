#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 23 09:34:06 2022

@author: Christoph PRUVOST
Formation Data Scientist OpenClassrooms - Projet n°7 

Code du tableau de bord, qui va communiquer avec l'API de prédiction.
"""

import streamlit as st
import requests
import pandas as pd
# import numpy as np

# Définition de variables
logo = 'static/logo.png'
# url_api = 'http://127.0.0.1:5000'
url_api = 'http://cpsolutions.eu.pythonanywhere.com'
endpoint_id_clients = url_api + '/clients/'
endpoint_data_client = endpoint_id_clients
endpoint_stats = url_api + '/stats/'
endpoint_prediction = url_api + '/predict/'
col_niv_info_1 = ['CODE_GENDER' , 'AMT_INCOME_TOTAL', 'AMT_CREDIT', 'AMT_ANNUITY' , \
                  'DAYS_BIRTH', 'DAYS_EMPLOYED', 'DAYS_REGISTRATION', 'CNT_FAM_MEMBERS']
resultat_prediction = None
type_info = None
affichage_resultats = False

# This must be the first Streamlit command used in your app, and must only be set once.
st.set_page_config(
    page_title="Prêt à dépenser - tableau de bord chargé de clientèle",
    page_icon=":AMT_ANNUITYmoney_with_wings:",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About" : 
        '''
        Tableau fait avec Streamlit, API faite avec Flask.
        
        Réalisation de Christoph Pruvost dans le cadre du projet n°7 de la formation Data Scientist OpenClassrooms
        [Plus d'informations](https://github.com/defrenes/P7)
        '''
    }
)

@st.cache
def recup_id_clients():
    """ Récupération des identifiants clients (numéros de dossiers)"""
    id_clients = requests.get(endpoint_id_clients).json()
    if id_clients:
        return id_clients['ids']
    else:
        return "Erreur lors du chargement des identifiants des clients (numéros de dossiers)"

@st.cache
def recup_infos_client(endpoint_data_client, num_dossier_client):
    """ Récupération des informations de la demande de prêt """
    infos_descriptives = requests.get(endpoint_data_client + str(num_dossier_client)).json()
    if infos_descriptives :
        return infos_descriptives
    else:
        return "Erreur lors de l'obtention de l'ensemble des données du prêt."

@st.cache
def recup_stats_client(endpoint_stats, num_dossier_client, variable):
    """ Récupération du graphique de la position du client au sein de la distribution d'une variable donnée. """
    graphique_comparatif = requests.get(endpoint_stats + str(num_dossier_client) + '/' + variable).content
    if graphique_comparatif :
        return graphique_comparatif
    else:
        return f"Erreur lors de l'obtention du graphique comparatif de la variable {variable} du dossier {num_dossier_client}."

@st.cache
def prediction(endpoint_prediction, num_dossier_client):
    """ Demande de prédiction à partir d'un idenfifiant client/numéro de dossier client """
    resultat_prediction = requests.get(endpoint_prediction + str(num_dossier_client)).json()
    if resultat_prediction :
        return resultat_prediction
    else:
        return "Erreur lors de l'obtention du résultat de la prédiction."


# Panneau latéral
with st.sidebar:
    num_dossier_client = st.selectbox(
        'Liste des dossiers clients disponibles :',
        recup_id_clients(),
        index=0,
        key='sk_id',
        help='Selectionner un numéro de dossier à étudier.')
    
    # Quelles type d'informations demande le chargé de clientèle ?
    type_info_1 = 'Résultat de la demande de prêt'
    type_info_2 = 'Informations descriptives du client'
    type_info_3 = 'Comparaison du client aux autres'
    type_info = st.radio(
        "Type d'informations souhaitées :",
        (type_info_1, type_info_2, type_info_3),
        key = 'type_info',
        help= 'Quelles informations souhaitez vous obtenir, entre le résultat de la demande de prêt,\
            les infomations dont nous disposons sur le client ou la situation du client par rapport aux autres clients.',
        )
        
    if type_info != type_info_1:
        # Si l'utilisateur sélectionne autre chose qu'une prédiction, il nous faut les informations client :
        infos_descriptives = recup_infos_client(endpoint_data_client, num_dossier_client)
        df = pd.DataFrame(infos_descriptives)
        if type_info == type_info_2:
            niv_info_1 = "Par défaut"
            niv_info_2 = "Sélection personnalisée"
            niv_info_3 = "Toutes les informations disponibles"
            choix_niveau_info = st.radio(
                "Niveau d'informations descriptives :",
                (niv_info_1, niv_info_2, niv_info_3),
                key = 'niv_info',
                help= 'Niveau de détail souhaité pour les informations descriptives \
                    (léger par défaut, plus détaillé en faisant une selection personnalisée, ou tout).',
                )
            if choix_niveau_info == niv_info_2:
                col_niv_info_2 = st.multiselect(
                    'Quelles informations souhaitez vous consulter ?',
                    df.columns.to_list(),
                    col_niv_info_1,
                    help="Saisissez le nom du ou des champs que vous souhaitez consulter pour ce client")
        else:
            niv_info_1 = "Par défaut"
            niv_info_2 = "Sélection personnalisée"
            choix_niveau_info = st.radio(
                "Niveau d'informations comparatives :",
                (niv_info_1, niv_info_2),
                key = 'niv_info',
                help= 'Niveau de détail souhaité pour les informations comparatives\
                    (léger par défaut, plus détaillé en faisant une selection personnalisée).',
                )
            if choix_niveau_info == niv_info_2:
                col_niv_info_2 = st.multiselect(
                    'Quelles informations souhaitez vous consulter ?',
                    df.columns.to_list(),
                    col_niv_info_1,
                    help="Saisissez le nom du ou des champs que vous souhaitez consulter pour ce client")

    if st.button('Valider', help="Valider le numéro de dossier."):
        affichage_resultats = True

# Panneau principal - activé par le bouton "valider"
st.title('Tableau de bord')
st.header('chargé de relation client')
if affichage_resultats == False:
    st.subheader("Mode d'emploi")
    st.markdown("""
                Pour continuer, sélectionnez dans la colonne en haut à gauche de l'écran : 
                1. le numéro de dossier client à étudier 
                1. les options éventuelles 
                1. validez vos choix pour afficher les résultats
                """)
    st.image(logo, caption='Logo société : Prêt à Dépenser', use_column_width='auto')
else:
    # Affichage de la prédiction concernant le remboursement du prêt par le client
    if type_info == type_info_1 :
        resultat_prediction = prediction(endpoint_prediction, num_dossier_client)
        with st.container():
            st.subheader(f"Prédiction pour le dossier {num_dossier_client}")
            st.header("Résultat de la prédiction :")
            col1, col2 = st.columns(2)
            with col1:
                if resultat_prediction['prediction'] == 0.0:
                    st.success("Le prêt est accordé.")
                elif resultat_prediction['prediction'] == 1.0:
                    st.error("Le prêt est refusé.")
            with col2:
                st.metric(label="Score", value=(str(int(100-resultat_prediction['score'])) + ' %'), delta=None)
    # Affichage des informations descriptives du client
    elif type_info == type_info_2 :
        if choix_niveau_info == niv_info_1:
            st.subheader(f"Informations descriptives par défaut pour le dossier {num_dossier_client}")
            tableau = st.table(df.loc[[str(num_dossier_client)], col_niv_info_1].T)
        elif choix_niveau_info == niv_info_2:
            st.subheader(f"Informations descriptives personnalisées pour le dossier {num_dossier_client}")
            tableau = st.table(df.loc[[str(num_dossier_client)], col_niv_info_2].T)
        else:
            st.subheader(f"Informations descriptives complètes pour le dossier {num_dossier_client}")
            tableau = st.table(df.loc[[str(num_dossier_client)]].T)
    # Affichage de données comparant le client à l'ensemble des clients
    elif type_info == type_info_3 :
        variable = 'DAYS_BIRTH'
        st.subheader(f"Informations comparatives par défaut pour le dossier {num_dossier_client}")
        if choix_niveau_info == niv_info_1:
            for variable in col_niv_info_1:
                graphique_comparatif = recup_stats_client(endpoint_stats, num_dossier_client, variable)
                st.image(graphique_comparatif, caption=f'Distribution de {variable}', use_column_width='auto')
        else:
            for variable in col_niv_info_2:
                graphique_comparatif = recup_stats_client(endpoint_stats, num_dossier_client, variable)
                st.image(graphique_comparatif, caption=f'Distribution de {variable}', use_column_width='auto')
                
# Affichage d'informations de débugage
# st.session_state
# st.write(affichage_resultats)