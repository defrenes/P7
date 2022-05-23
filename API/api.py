#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 20 14:38:41 2022

@author: Christoph PRUVOST
Formation Data Scientist OpenClassrooms - Projet n°7 
"""
import os
from flask import Flask, jsonify #, request , render_template
import pandas as pd
import joblib
# import requests

# Variables
data_dir    = '.data'
data_prod   = 'data_prod.ftr'
modele_prod = 'modele_api.joblib'

modele = joblib.load(os.path.join(data_dir, modele_prod))
df = pd.read_feather(os.path.join(data_dir, data_prod))
# Utilisation de SK_ID_CURR comme index pour faciliter les recherches dans le DF.
df.set_index(df.SK_ID_CURR, drop=True, inplace=True, verify_integrity=True)
var_non_predictives = ["index", "SK_ID_CURR", "SK_ID_BUREAU", "SK_ID_PREV", "TARGET"] 
var_predictives = [col for col in df.columns if col not in var_non_predictives]

X = df[var_predictives]


app = Flask(__name__)

@app.route("/", methods=['GET'])
def hello():
    return "Hello World!"

@app.route("/clients/", methods=['GET'])
def clients(X):
    """
    Renvoie la liste des identifiants uniques des dossiers clients : SK_ID_CURR
    exemple de requête : http://127.0.0.1:5000/clients/
    """
    # Limitons la liste à 10 ID pour le développement :
    ids = X.index.to_list()[:10]
    return jsonify({
        'ids' : ids
        })

@app.route('/predict/<int:id>/', methods=['GET'])
def predict(id):
    """
    exemple de requête : http://127.0.0.1:5000/predict/4130033/
    
    Returns
    -------
    id : int
        Numéro du dossier
    TYPE
        DESCRIPTION.
    """
    donnees_client = X.loc[[id]]
    score_client = 100 * modele.predict_proba(donnees_client)[0][1]
    prediction = modele.predict(donnees_client)[0]

    return jsonify({
        'id': id,
        'score' : score_client,
        'prediction' : prediction
        })

if __name__ == "__main__":
    app.run(debug=True)
