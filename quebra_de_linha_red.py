import pandas as pd
import json
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_pymongo import PyMongo
from credentials import settings, credenciais, secret_jwt
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import os
import re
import jwt


app = Flask("Delta Goal")
CORS(app)
app.config["SECRET_KEY"] = "dg123"
app.config[
    "MONGO_URI"
] = f"mongodb+srv://{credenciais['user_mongo']}:{credenciais['password_mongo']}@{settings['host']}/{settings['database']}?retryWrites=true&w=majority"
mongo = PyMongo(app)
bcrypt = Bcrypt(app)

partidas = mongo.db.partidas
modelo_quebra_linha = partidas.find_one({"nome": "modelo_quebra_linha"})
data = modelo_quebra_linha

rupturas_pal = data["time"]["1"]["rupturas"]
rupturas_red = data["time"]["5"]["rupturas"]

for ruptura in rupturas_red:
    print(ruptura)

dic_rupturas_red = {}
zonas_ataque_red = {}

for ruptura in rupturas_red:
    if ruptura["zona_defesa"] not in zonas_ataque_red:
        zonas_ataque_red[ruptura["zona_defesa"]] = 1
    else:
        zonas_ataque_red[ruptura["zona_defesa"]] += 1

    if ruptura["nome_jogador_ruptura"] not in dic_rupturas_red:
        dic_rupturas_red[ruptura["nome_jogador_ruptura"]] = {
            "tempo_ruptura": [ruptura["instante_ruptura"]],
            "jogador_posse_de_bola": [ruptura["nome_jogador_posse_bola"]],
            "desfecho": [ruptura["desfecho"]],
            "qntd_rupturas": 1,
            "zona": [ruptura["zona_defesa"]],
            "time": "Bragantino",
        }
    else:
        dic_rupturas_red[ruptura["nome_jogador_ruptura"]]["tempo_ruptura"].append(
            ruptura["instante_ruptura"]
        )
        dic_rupturas_red[ruptura["nome_jogador_ruptura"]]["desfecho"].append(
            ruptura["desfecho"]
        )
        dic_rupturas_red[ruptura["nome_jogador_ruptura"]]["zona"].append(
            ruptura["zona_defesa"]
        )
        dic_rupturas_red[ruptura["nome_jogador_ruptura"]][
            "jogador_posse_de_bola"
        ].append(ruptura["nome_jogador_posse_bola"])
        dic_rupturas_red[ruptura["nome_jogador_ruptura"]]["qntd_rupturas"] += 1

dic_rupturas_red


ZONAS_ATAQUE_RED = zonas_ataque_red

DF_BRAGANTINO = pd.DataFrame(dic_rupturas_red)
DF_BRAGANTINO = DF_BRAGANTINO
desfechos_red = {}
for lista_desfechos_red in DF_BRAGANTINO.iloc[2]:
    for desfecho in lista_desfechos_red:
        if desfecho in desfechos_red.keys():
            desfechos_red[desfecho] += 1
        else:
            desfechos_red[desfecho] = 1

DF_BRAGANTINO = pd.DataFrame(dic_rupturas_red)
DF_BRAGANTINO = DF_BRAGANTINO.transpose()
# DF_BRAGANTINO
