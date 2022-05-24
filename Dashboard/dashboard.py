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
import numpy as np

# Définition de variables
url_api = 'http://127.0.0.1:5000'
endpoint_id_clients = url_api + '/clients/'
endpoint_data_client = endpoint_id_clients
endpoint_prediction = url_api + '/predict/'
resultat_prediction  = None
col_niv_info_1 = ['CODE_GENDER' , 'AMT_INCOME_TOTAL', 'AMT_CREDIT', 'AMT_ANNUITY' , 'NAME_FAMILY_STATUS',\
                  'NAME_HOUSING_TYPE', 'DAYS_BIRTH', 'DAYS_EMPLOYED', 'DAYS_REGISTRATION', 'CNT_FAM_MEMBERS']

@st.cache
def recup_id_clients():
    """ Récupération des identifiants clients (numéros de dossiers)"""
    #response = fetch(session, f"http://fastapi:8008/api/clients")
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
def prediction(endpoint_prediction, num_dossier_client):
    """ Demande de prédiction à partir d'un idenfifiant client/numéro de dossier client """
    resultat_prediction = requests.get(endpoint_prediction + str(num_dossier_client)).json()
    if resultat_prediction :
        return resultat_prediction
    else:
        return "Erreur lors de l'obtention du résultat de la prédiction."


st.title('Tableau de bord')

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write("here data")
    
    
df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
    })

# Panneau latéral
with st.sidebar:
    
    num_dossier_client = st.selectbox(
        'Liste des dossiers clients disponibles :',
        recup_id_clients(), #df['first column'],
        index=0,
        key='sk_id',
        help='Selectionner un numéro de dossier à étudier.')
    
    st.write('Dossier selectionné : ', num_dossier_client)
    
    if st.button('Lancer la prédiction', help="Lancer la prédiction."):
        resultat_prediction = prediction(endpoint_prediction, num_dossier_client)
        st.write('Prédiction lancée...')
        st.write(resultat_prediction['score'])
    else:
        st.write('En attente du choix du numéro de dossier et du lancement de la prédiction...')

    # Afficher des informations descriptives ?
    checkbox_infos_descriptives = st.checkbox(
        'Afficher des informations descriptives sur le client',
        value=False,
        help="Afficher des informations descriptives par défaut pour ce dossier client."
        )
    if checkbox_infos_descriptives:
        st.write(st.session_state.sk_id)
        niv_info_1 = "Par défaut"
        niv_info_2 = "Sélection personnalisée"
        choix_niveau_info = st.radio(
            "Niveau d'information :",
            (niv_info_1, niv_info_2),
            help = 'Niveau de détail souhaité pour les informations descriptives \
                (léger par défaut ou plus détaillé en faisant une selection personnalisée).',
            )
        infos_descriptives = recup_infos_client(endpoint_data_client, num_dossier_client)
        df = pd.DataFrame(infos_descriptives)


# Panneau principal - activé par la prédiction
if resultat_prediction != None:
    with st.container():
        st.header("Résultat de la prédiction :")
        col1, col2 = st.columns(2)
        with col1:
            if resultat_prediction['prediction'] == 0.0:
                st.success("Le prêt est accordé.")
            elif resultat_prediction['prediction'] == 1.0:
                st.error("Le prêt est refusé.")
        with col2:
            st.metric(label="Score", value=(str(100-int(resultat_prediction['score'])) + ' %'), delta=None)
        
        if checkbox_infos_descriptives:     
            if choix_niveau_info == niv_info_1:
                st.write(choix_niveau_info)
                tableau = st.table(df.loc[[num_dossier_client], col_niv_info_1])
            else:
                st.write(choix_niveau_info)
                
            
            tableau = st.table(df)
          
    st.write("En dehors du panneau principal")