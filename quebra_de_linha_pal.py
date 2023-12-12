import pandas as pd
import json

with open("dados/QuebraLinha_Palmeiras_x_Bragantino.json") as f:
    data = json.load(f)

rupturas_pal = data["time"]["1"]["rupturas"]
rupturas_red = data["time"]["5"]["rupturas"]

for ruptura in rupturas_pal:
    print(ruptura)

dic_rupturas_pal = {}
zonas_ataque_pal = {}

for ruptura in rupturas_pal:
    if ruptura["zona_defesa"] not in zonas_ataque_pal:
        zonas_ataque_pal[ruptura["zona_defesa"]] = 1
    else:
        zonas_ataque_pal[ruptura["zona_defesa"]] += 1

    if ruptura["nome_jogador_ruptura"] not in dic_rupturas_pal:
        dic_rupturas_pal[ruptura["nome_jogador_ruptura"]] = {
            "tempo_ruptura": [ruptura["instante_ruptura"]],
            "jogador_posse_de_bola": [ruptura["nome_jogador_posse_bola"]],
            "desfecho": [ruptura["desfecho"]],
            "qntd_rupturas": 1,
            "zona": [ruptura["zona_defesa"]],
            "time": "Palmeiras",
        }

    else:
        dic_rupturas_pal[ruptura["nome_jogador_ruptura"]]["tempo_ruptura"].append(
            ruptura["instante_ruptura"]
        )
        dic_rupturas_pal[ruptura["nome_jogador_ruptura"]]["desfecho"].append(
            ruptura["desfecho"]
        )
        dic_rupturas_pal[ruptura["nome_jogador_ruptura"]]["zona"].append(
            ruptura["zona_defesa"]
        )
        dic_rupturas_pal[ruptura["nome_jogador_ruptura"]][
            "jogador_posse_de_bola"
        ].append(ruptura["nome_jogador_posse_bola"])
        dic_rupturas_pal[ruptura["nome_jogador_ruptura"]]["qntd_rupturas"] += 1

ZONAS_ATAQUE_PAL = zonas_ataque_pal

DF_PALMEIRAS = pd.DataFrame(dic_rupturas_pal)
DF_PALMEIRAS = DF_PALMEIRAS
desfechos_pal = {}
for lista_desfechos_pal in DF_PALMEIRAS.iloc[2]:
    for desfecho in lista_desfechos_pal:
        if desfecho in desfechos_pal.keys():
            desfechos_pal[desfecho] += 1
        else:
            desfechos_pal[desfecho] = 1

# DF_PALMEIRAS
DF_PALMEIRAS = pd.DataFrame.to_json(DF_PALMEIRAS)
