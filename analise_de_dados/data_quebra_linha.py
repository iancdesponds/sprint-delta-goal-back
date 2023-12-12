import pandas as pd
import json

with open("dados/QuebraLinha_Palmeiras_x_Bragantino.json") as f:
    data = json.load(f)

quebra_linha_pal = data["time"]["1"]["rupturas"]
quebra_linha_red = data["time"]["5"]["rupturas"]
num_quebra_linha_pal = 0

for quebra_linha in quebra_linha_pal:
    num_quebra_linha_pal += 1

dic_quebra_linha_pal = {}

for quebra_linha in quebra_linha_pal:
    quebra_linha_instante = quebra_linha["instante_ruptura"]

    dic_quebra_linha_pal[quebra_linha_instante] = {
        "nome_jogadores_time_atacando": quebra_linha["nome_jogador_ruptura"],
        "nome_jogadores_time_defendendo": quebra_linha["nomes_jogadores_defesa"],
        "desfecho": quebra_linha["desfecho"],
        "zona": quebra_linha["zona_defesa"]
    }

df_ql_pal = pd.DataFrame(dic_quebra_linha_pal)
df_ql_pal = df_ql_pal.transpose()
df_ql_pal['instante_inicial'] = df_ql_pal.index
df_ql_pal.reset_index(drop=True, inplace=True)

df_nome_jogadores_time_atacando_pal = df_ql_pal['nome_jogadores_time_atacando']

dic_nome_jogadores_time_atacando_pal = {}

for nome_jogador in df_nome_jogadores_time_atacando_pal:
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
        if nome not in dic_nome_jogadores_time_atacando_pal:
            dic_nome_jogadores_time_atacando_pal[nome] = 1
        else:
            dic_nome_jogadores_time_atacando_pal[nome] += 1

df_destaques_ql_pal = pd.DataFrame(dic_nome_jogadores_time_atacando_pal.items(), columns=['nome_jogador', 'num_participacoes_em_quebras_linha'])
df_destaques_ql_pal = df_destaques_ql_pal.sort_values(by='num_participacoes_em_quebras_linha', ascending=False)
df_destaques_ql_pal = df_destaques_ql_pal.reset_index(drop=True)

# BRAGANTINO

num_quebra_linha_red = 0  

for quebra_linha in quebra_linha_red:
    num_quebra_linha_red += 1

dic_quebra_linha_red = {}

for quebra_linha in quebra_linha_red:
    quebra_linha_instante = quebra_linha["instante_ruptura"]

    dic_quebra_linha_red[quebra_linha_instante] = {
        "nome_jogadores_time_atacando": quebra_linha["nome_jogador_ruptura"],
        "nome_jogadores_time_defendendo": quebra_linha["nomes_jogadores_defesa"],
        "desfecho": quebra_linha["desfecho"],
        "zona": quebra_linha["zona_defesa"]
    }

df_ql_red = pd.DataFrame(dic_quebra_linha_red)
df_ql_red = df_ql_red.transpose()
df_ql_red['instante_inicial'] = df_ql_red.index
df_ql_red.reset_index(drop=True, inplace=True)

df_nome_jogadores_time_atacando_red = df_ql_red['nome_jogadores_time_atacando']

dic_nome_jogadores_time_atacando_red = {}

for nome_jogador in df_nome_jogadores_time_atacando_red:
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
        if nome not in dic_nome_jogadores_time_atacando_red:
            dic_nome_jogadores_time_atacando_red[nome] = 1
        else:
            dic_nome_jogadores_time_atacando_red[nome] += 1

df_destaques_ql_red = pd.DataFrame(dic_nome_jogadores_time_atacando_red.items(), columns=['nome_jogador', 'num_participacoes_em_quebras_linha'])
df_destaques_ql_red = df_destaques_ql_red.sort_values(by='num_participacoes_em_quebras_linha', ascending=False)
df_destaques_ql_red = df_destaques_ql_red.reset_index(drop=True)
