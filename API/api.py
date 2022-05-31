#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 20 14:38:41 2022

@author: Christoph PRUVOST
Formation Data Scientist OpenClassrooms - Projet n°7 
"""
import os
from flask import Flask, jsonify, send_file #, request , render_template
import pandas as pd
import joblib
from io import BytesIO
from matplotlib.figure import Figure
import seaborn as sns

# Variables
data_dir    = 'data'
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
    """
    Route basique pour vérifier le bon fonctionnement de l'API.
    Exemple de requête : http://127.0.0.1:5000
    """
    return "Hello World!"

@app.route("/clients/", methods=['GET'])
def clients():
    """
    Renvoie la liste des identifiants uniques des dossiers clients : SK_ID_CURR
    Exemple de requête : http://127.0.0.1:5000/clients
    """
    # Limitation de la liste à 10 ID pour le développement : ids = X.index.to_list()[:10]
    ids = X.index.to_list()
    return jsonify({
        'ids' : ids
        })

@app.route("/clients/<int:id>", methods=['GET'])
def details_client(id):
    """
    Renvoie l'ensemble des informations d'un dossier client.
    Exemple de requête : http://127.0.0.1:5000/clients/161095
    """
    dossier_client = X.loc[[id]]
    return dossier_client.to_json()

@app.route("/stats/<int:id>/<variable>", methods=['GET'])
def distribution_client(id, variable):
    """
    Renvoie une image contenant un graphique de la distribution d'une variable
    reçue en paramètre, avec la situation du client par rapport à la distribution.
    Exemple de requête : http://127.0.0.1:5000/stats/161095/DAYS_BIRTH
    """
    # Generate the figure **without using pyplot** by using Figure
    fig = Figure(figsize=(7,4))
    ax = fig.subplots()
    sns.histplot(
                data=df,
                x=variable,
                hue="TARGET",
                cumulative=False,
                multiple='stack',
                legend=False,
                ax=ax)
    ax.axvline(x=df.loc[[id],[variable]].values[0][0], color='red', lw=2, linestyle='--', label='client')
    fig.legend(loc='upper left',
               fontsize='small',
               bbox_to_anchor=(0.13, 0.88),
               labels=[f'Dossier client {id}', 'Défauts de paiement', 'Remboursements réussis'])
    fig.suptitle(f"Positionnement du client dans la distribution de \n{variable}")
    bytes_image = BytesIO()
    fig.savefig(bytes_image, format='png')
    bytes_image.seek(0)
    return send_file(bytes_image,
                     download_name='plot.png',
                     as_attachment=False,
                     mimetype='image/png')

@app.route('/predict/<int:id>', methods=['GET'])
def predict(id):
    """
    Prédiction du défaut de paiement ou non d'un dossier client.
    Retourne au format JSON le numéro de dosser, son score sur 100 et la classe (0 validé/1 refusé).
    exemple de requête : http://127.0.0.1:5000/predict/413003
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