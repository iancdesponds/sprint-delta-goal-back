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
modelo_cruzamentos = partidas.find_one({"nome": "modelo_cruzamentos"})

data = modelo_cruzamentos


cruzamentos_pal = (data["time"]["1"]["rupturas"])
cruzamentos_red = (data["time"]["5"]["rupturas"])
num_cruzamentos_pal = 0

for cruzamento in cruzamentos_pal:
    num_cruzamentos_pal += 1
    # print(cruzamento)

dic_cruzamentos_pal = {} 

for cruzamento in cruzamentos_pal:
    cruzamento_instante = cruzamento["instante_cruzamento"]

    dic_cruzamentos_pal[cruzamento_instante] = {
        "nome_jogadores_time_cruzando": cruzamento["nome_jogadores_time_cruzando"],
        "nome_jogadores_time_defendendo": cruzamento["nome_jogadores_time_defendendo"],
        "desfecho": cruzamento["desfecho"],
        "zona": cruzamento["zona"]
    }



df_pal = pd.DataFrame(dic_cruzamentos_pal)
df_pal = df_pal.transpose()
df_pal['instante_inicial'] = df_pal.index
df_pal.reset_index(drop=True, inplace=True)

# Destaques em participações em cruzamentos do Palmeiras
df_nome_jogadores_time_cruzando_pal = df_pal['nome_jogadores_time_cruzando']

dic_nome_jogadores_time_cruzando_pal = {}

for nome_jogador in df_nome_jogadores_time_cruzando_pal:
    # Remover espaços extras no início e no final
    nome_jogador = nome_jogador.strip()
    # Espaços antes e depois das vírgulas
    nome_jogador = nome_jogador.replace(" , ", ",")
    # Tirar espaços em branco depois das vírgulas
    nome_jogador = nome_jogador.replace(", ", ",")
    # Ou espaço antes das vírgulas
    nome_jogador = nome_jogador.replace(" ,", ",")
    # Separar os nomes
    nomes = nome_jogador.split(",")
    for nome in nomes:
        # Remover espaços extras no início e no final de cada nome
        nome = nome.strip()
        if nome not in dic_nome_jogadores_time_cruzando_pal:
            dic_nome_jogadores_time_cruzando_pal[nome] = 1
        else:
            dic_nome_jogadores_time_cruzando_pal[nome] += 1

df_destaques_pal = pd.DataFrame(dic_nome_jogadores_time_cruzando_pal.items(), columns=['nome_jogador', 'num_participacoes_em_cruzamentos'])
df_destaques_pal = df_destaques_pal.sort_values(by='num_participacoes_em_cruzamentos', ascending=False)
df_destaques_pal = df_destaques_pal.reset_index(drop=True)


### Bragantino

num_cruzamentos_red = 0
for cruzamento in cruzamentos_red:
    num_cruzamentos_red += 1

dic_cruzamentos_red = {}

for cruzamento in cruzamentos_red:
    cruzamento_instante = cruzamento["instante_cruzamento"]

    dic_cruzamentos_red[cruzamento_instante] = {
        "nome_jogadores_time_cruzando": cruzamento["nome_jogadores_time_cruzando"],
        "nome_jogadores_time_defendendo": cruzamento["nome_jogadores_time_defendendo"],
        "desfecho": cruzamento["desfecho"],
        "zona": cruzamento["zona"]
    }

df_red = pd.DataFrame(dic_cruzamentos_red)
df_red = df_red.transpose()
df_red['instante_inicial'] = df_red.index
df_red.reset_index(drop=True, inplace=True)

# Destaques em participações em cruzamentos do Bragantino
df_nome_jogadores_time_cruzando_red = df_red['nome_jogadores_time_cruzando']

dic_nome_jogadores_time_cruzando_red = {}

for nome_jogador in df_nome_jogadores_time_cruzando_red:
    # Remover espaços extras no início e no final
    nome_jogador = nome_jogador.strip()
    # Espaços antes e depois das vírgulas
    nome_jogador = nome_jogador.replace(" , ", ",")
    # Tirar espaços em branco depois das vírgulas
    nome_jogador = nome_jogador.replace(", ", ",")
    # Ou espaço antes das vírgulas
    nome_jogador = nome_jogador.replace(" ,", ",")
    # Separar os nomes
    nomes = nome_jogador.split(",")
    for nome in nomes:
        # Remover espaços extras no início e no final de cada nome
        nome = nome.strip()
        if nome not in dic_nome_jogadores_time_cruzando_red:
            dic_nome_jogadores_time_cruzando_red[nome] = 1
        else:
            dic_nome_jogadores_time_cruzando_red[nome] += 1

# DataFrame de destaques em participações em cruzamentos do Bragantino
df_destaques_red = pd.DataFrame(dic_nome_jogadores_time_cruzando_red.items(), columns=['nome_jogador', 'num_participacoes_em_cruzamentos'])
df_destaques_red = df_destaques_red.sort_values(by='num_participacoes_em_cruzamentos', ascending=False)
df_destaques_red = df_destaques_red.reset_index(drop=True)


#########################################

def contar_zonas_repetidas(dados,time):
    time_rupturas = dados["time"][time]["rupturas"]
    zonas_repetidas = {}

    for ruptura in time_rupturas:
        zona = ruptura["zona"]

        if zona in zonas_repetidas:
            zonas_repetidas[zona] += 1
        else:
            zonas_repetidas[zona] = 1

    return zonas_repetidas

def calculate_zone_percentages(dados,time):
    dicionario=contar_zonas_repetidas(dados,time)
    total=0
    for quantidade in dicionario.values():
        total+=quantidade
    for zona, cruzamento in dicionario.items():
        dicionario[zona]=f"{(cruzamento/total)*100:.1f}%"
    return dicionario

zonas_cuzamentos_pal = calculate_zone_percentages(data,'1')
# print(zonas_cuzamentos_pal)
zonas_cuzamentos_red= calculate_zone_percentages(data,'5')
# print(zonas_cuzamentos_red)

##################################################

desfechos_cruzamentos_pal = df_pal['desfecho']
desfechos_cruzamentos_pal = desfechos_cruzamentos_pal.reset_index(drop=True)
desfechos_cruzamentos_pal = desfechos_cruzamentos_pal.to_dict()
quant_desfechos_cruzamentos_pal = {}
for desfecho in desfechos_cruzamentos_pal.values():
    if desfecho not in quant_desfechos_cruzamentos_pal:
        quant_desfechos_cruzamentos_pal[desfecho] = 1
    else:
        quant_desfechos_cruzamentos_pal[desfecho] += 1


desfechos_cruzamentos_red = df_red['desfecho']
desfechos_cruzamentos_red = desfechos_cruzamentos_red.reset_index(drop=True)
desfechos_cruzamentos_red = desfechos_cruzamentos_red.to_dict()
quant_desfechos_cruzamentos_red = {}
for desfecho in desfechos_cruzamentos_red.values():
    if desfecho not in quant_desfechos_cruzamentos_red:
        quant_desfechos_cruzamentos_red[desfecho] = 1
    else:
        quant_desfechos_cruzamentos_red[desfecho] += 1

