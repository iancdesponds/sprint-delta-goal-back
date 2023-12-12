# Importando bibliotecas
import pandas as pd
import scipy.stats as st
import numpy as np
import matplotlib.pyplot as plt
import math
import json

# Função para leiura dos dados
def dados(caminho_do_arquivo):
    # Leitura dos dados
    df = pd.read_csv(caminho_do_arquivo)
    
    # Ordena os dados por frame e tempo do jogador
    df = df.sort_values(by=['FRAME', 'TIME_JOGADOR'])
    
    return df

# Função para obter os IDs dos times, como exemplo: RED e PAL.
def obtem_times(df):
    df = df[df['OBJETO_OBSERVADO'] == 'jogador']
    times = df['TIME_JOGADOR'].unique().tolist()
    return times

# Função para a criação de colunas para indicar se a bola está dentro da área (lados direito e esquerdo)
def colunas_bola_dentro_das_areas(df_bola):
    # Cria cópias dos DataFrames
    df_bola = df_bola.copy()

    # Cria colunas para indicar se a bola está dentro da área
    df_bola["DENTRO_AREA_DIREITA"] = 0
    df_bola["DENTRO_AREA_ESQUERDA"] = 0

    # Define as áreas
    area_direita = (df_bola["X"] > 101.5) & (df_bola["Y"] > 17.85) & (df_bola["Y"] < 58.15)
    df_bola.loc[area_direita, "DENTRO_AREA_DIREITA"] = 1
    area_esquerda = (df_bola["X"] < 16.5) & (df_bola["Y"] > 17.85) & (df_bola["Y"] < 58.15)
    df_bola.loc[area_esquerda, "DENTRO_AREA_ESQUERDA"] = 1

    # DataFrame com os dados da bola
    df_bola = df_bola.sort_values(by=['TEMPO_JOGO', 'FRAME'])
    df_bola.reset_index(drop=True, inplace=True)

    return df_bola

# Função para identificar o lado do ataque (direita ou esquerda) de acordo com o tempo de jogo
def identifica_lado_do_ataque(df, id_time, tempo_jogo):

    # Primeiro e último frames
    primeiro_frame = df['FRAME'].min() # 1º tempo de jogo
    ultimo_frame = df['FRAME'].max() # 2º tempo de jogo

    if tempo_jogo == 1:
        pos_goleiro = df[(df['FRAME'] == primeiro_frame) & (df['OBJETO_OBSERVADO'] == 'jogador') & (df['POSICAO_JOGADOR'] == 'Goleiro') & (df['TIME_JOGADOR'] == id_time)]
    if tempo_jogo == 2:
        pos_goleiro = df[(df['FRAME'] == ultimo_frame) & (df['OBJETO_OBSERVADO'] == 'jogador') & (df['POSICAO_JOGADOR'] == 'Goleiro') & (df['TIME_JOGADOR'] == id_time)]
    
    if not pos_goleiro.empty:
        x_goleiro = pos_goleiro.iloc[0]['X']
        
        # Determinar o do ataque baseado na posição do goleiro dado o tempo de jogo
        if x_goleiro < 59:  # 118/2 (meio do campo)
            return 'DIREITA'
        else:
            return 'ESQUERDA'
    else:
        return None

# Função que retorna um dicionário com as zonas do campo (origem dos cruzamentos)
def definir_zonas(lado_ataque):
    if lado_ataque == 'DIREITA':
        zonas = {
            'E1.2':{
            'X0': 86.5,
            'X1': 101.5,
            'Y0': 0,
            'Y1': 17.85,
            'num': 0
            },
            'E1.1':{
                'X0': 86.5,
                'X1': 101.5,
                'Y0': 17.85,
                'Y1': 38,
                'num': 0
            },
            'E2.1':{
                'X0': 101.5,
                'X1': 109.75,
                'Y0': 0,
                'Y1': 17.85,
                'num': 0
            },
            'E2.2':{
                'X0': 109.75,
                'X1': 118,
                'Y0': 0,
                'Y1': 17.85,
                'num': 0
            },
            'E3':{
                'X0': 101.5,
                'X1': 109.75,
                'Y0': 17.85,
                'Y1': 27.92,
                'num': 0
            },
            'D1.1':{
                'X0': 86.5,
                'X1': 101.5,
                'Y0': 38,
                'Y1': 58.15,
                'num': 0
            },
            'D1.2':{
                'X0': 86.5,
                'X1': 101.5,
                'Y0': 58.15,
                'Y1': 76,
                'num': 0
            },
            'D2.1':{
                'X0': 101.5,
                'X1': 109.75,
                'Y0': 58.15,
                'Y1': 76,
                'num': 0
            },
            'D2.2':{
                'X0': 109.75,
                'X1': 118,
                'Y0': 58.15,
                'Y1': 76,
                'num': 0
            },
            'D3':{
                'X0': 101.5,
                'X1': 109.75,
                'Y0': 48.07,
                'Y1': 58.15,
                'num':0
            }
        }
    elif lado_ataque == 'ESQUERDA':
        zonas = {
            'E1.2':{
            'X0': 16.5,
            'X1': 31.5,
            'Y0': 58.15,
            'Y1': 75,
            'num': 0
            },
            'E1.1':{
                'X0': 16.5,
                'X1': 31.5,
                'Y0': 38,
                'Y1': 58.15,
                'num': 0
            },
            'E2.1':{
                'X0': 8.25,
                'X1': 16.5,
                'Y0': 58.15,
                'Y1': 75,
                'num': 0
            },
            'E2.2':{
                'X0': 0,
                'X1': 8.25,
                'Y0': 58.15,
                'Y1': 75,
                'num': 0
            },
            'E3':{
                'X0': 8.25,
                'X1': 16.5,
                'Y0': 48.07,
                'Y1': 58.15,
                'num': 0
            },
            'D1.1':{
                'X0': 16.5,
                'X1': 31.5,
                'Y0': 17.85,
                'Y1': 38,
                'num': 0
            },
            'D1.2':{
                'X0': 16.5,
                'X1': 31.5,
                'Y0': 1,
                'Y1': 17.85,
                'num': 0
            },
            'D2.1':{
                'X0': 8.25,
                'X1': 16.5,
                'Y0': 1,
                'Y1': 17.85,
                'num': 0
            },
            'D2.2':{
                'X0': 0,
                'X1': 8.25,
                'Y0': 1,
                'Y1': 17.85,
                'num': 0
            },
            'D3':{
                'X0': 8.25,
                'X1': 16.5,
                'Y0': 17.85,
                'Y1': 27.92,
                'num': 0
            }
        }
    else:
        raise ValueError("Lado do ataque inválido.")

    return zonas

# Função para análise inicial de cruzamentos
def primeira_analise_cruzamentos(df_bola, df_jogadores, zonas, lado_ataque, area_de_ataque, duracao_lim=20):
    contador = 0
    frames_teste = []

    for index, row in df_jogadores.iterrows():
        if index + 1 == len(df_jogadores): # Verifica se é o último frame
            break
        if (df_jogadores.iloc[index+1][area_de_ataque] == 1 and row[area_de_ataque] == 0): # Verifica se a bola entrou na área
            sequencia_de_1 = 0
            for i in range(1, duracao_lim+1):
                if index + i == len(df_jogadores):
                    break
                if df_jogadores.iloc[index+i][area_de_ataque] == 1:
                    sequencia_de_1 += 1
                if sequencia_de_1 == duracao_lim:
                    for zona in zonas:
                        if (df_jogadores.iloc[index-50]["X"] > zonas[zona]["X0"] and df_jogadores.iloc[index-50]["X"] < zonas[zona]["X1"] and df_jogadores.iloc[index-50]["Y"] > zonas[zona]["Y0"] and df_jogadores.iloc[index-50]["Y"] < zonas[zona]["Y1"]):
                            contador += 1
                            frames_teste.append(df_jogadores.iloc[index+1]["FRAME"])
                            break
                    break

    return contador, frames_teste

# Função que retorna um dicionário com os jogadores que cruzaram e o frame que cruzaram (mais precisa que a função anterior)
def analise_final_cruzamentos(df_bola, df_jogadores, zonas, frames_teste, lado_ataque, duracao_lim=20, distancia_lim=4):
    jogadores_que_cruzaram = {}
    velocidades_maximas = {}
    frames_finais = []
    zonas_ = []
    cruzamentos = 0

    for frame in frames_teste:
        # Variáveis
        x_bola = 0
        y_bola = 0
        velocidade_bola = 0
        distancia_entre_jogador_e_bola = 100 # Valor inicial alto para que qualquer distância seja menor que ele

        # DataFrame com os dados da bola no intervalo do cruzamento (frame e 2 segundos antes)
        df_frame_bola = df_jogadores[(df_jogadores['FRAME'] <= frame) & (df_jogadores['FRAME'] >= frame-50) & (df_jogadores['OBJETO_OBSERVADO'] == 'bola')]

        for index, row in df_frame_bola.iterrows():
            if row['VELOCIDADE'] > velocidade_bola:
                velocidade_bola = row['VELOCIDADE'] # Determina a velocidade máxima da bola no intervalo
                frame_que_cruzou = row['FRAME'] # Determina o frame em que a bola atinge a velocidade máxima
                # Coordenadas da bola no momento do cruzamento
                x_bola = row['X']
                y_bola = row['Y']

        # Velocidades máximas atingidas pela bola em cada cruzamento (momento em que o jogador toca na bola)
        velocidades_maximas[frame_que_cruzou] = velocidade_bola

        # Mesmo DataFrame, mas com os dados dos jogadores
        df_frame_jogadores = df_jogadores[(df_jogadores['FRAME'] <= frame) & (df_jogadores['FRAME'] >= frame-50) & (df_jogadores['OBJETO_OBSERVADO'] == 'jogador')]

        for index, row in df_frame_jogadores.iterrows():
            pos_jogador = [row['X'], row['Y']] # Coordenadas do jogador
            pos_bola = [x_bola, y_bola] # Coordenadas da bola
            distancia_medida = math.dist(pos_jogador, pos_bola) # Distância entre o jogador e a bola: distância de dois pontos
            if distancia_medida < distancia_entre_jogador_e_bola: # A menor distância é a que o jogador toca na bola (cruza)
                distancia_entre_jogador_e_bola = distancia_medida
                jogador = row['NOME_JOGADOR'] # Nome do jogador que cruzou

        for zona in zonas:
            # Verifica se o cruzamento ocorreu em alguma das zonas
            if x_bola > zonas[zona]['X0'] and x_bola < zonas[zona]['X1'] and y_bola > zonas[zona]['Y0'] and y_bola < zonas[zona]['Y1']:
            # Verificar se a variação da posição da bola no eixo x em 3 segundos antes do toque é maior que 4 metros
                if df_jogadores[(df_jogadores['FRAME'] <= frame_que_cruzou) & (df_jogadores['FRAME'] >= frame_que_cruzou-75) & (df_jogadores['OBJETO_OBSERVADO'] == 'bola')]['X'].max() - df_jogadores[(df_jogadores['FRAME'] <= frame_que_cruzou) & (df_jogadores['FRAME'] >= frame_que_cruzou-100) & (df_jogadores['OBJETO_OBSERVADO'] == 'bola')]['X'].min() > 4:
                    cruzamentos += 1
                    frames_finais.append(frame_que_cruzou)
                    zonas_.append(zona)
                    # Adiciona o jogador que cruzou a bola no dicionário
                    if jogador in jogadores_que_cruzaram:
                        jogadores_que_cruzaram[jogador].append(frame_que_cruzou)
                    else:
                        jogadores_que_cruzaram[jogador] = [frame_que_cruzou]
                    break

    return cruzamentos, frames_finais, jogadores_que_cruzaram, velocidades_maximas, zonas_

# Função para obter a zona/origem de cada cruzamento
def obter_zona_cruzamento(df, frame, zonas, tempo_jogo):
    df_tempo = df[df['TEMPO_JOGO'] == tempo_jogo]
    df_frame = df_tempo[df_tempo['FRAME'] == frame]
    x_bola = df_frame['X'].values[0]
    y_bola = df_frame['Y'].values[0]

    for zona in zonas:
        if x_bola > zonas[zona]['X0'] and x_bola < zonas[zona]['X1'] and y_bola > zonas[zona]['Y0'] and y_bola < zonas[zona]['Y1']:
            return zona
        
# Função para obter o desfecho de cada cruzamento
def obter_desfecho_cruzamentos(df, frame, id_time, times, tempo_jogo):
    df = df[df['OBJETO_OBSERVADO'] == 'bola']
    df_tempo = df[df['TEMPO_JOGO'] == tempo_jogo]
    frame_desfecho = df_tempo[df_tempo['FRAME'] == frame + 60]
    frame_cruzamento = df_tempo[df_tempo['FRAME'] == frame]

    if id_time == times[0]:
        time1 = times[0]
        time2 = times[1]
    elif id_time == times[1]:
        time1 = times[1]
        time2 = times[0]

    for i in range(60):
        frame_apos = df_tempo[df_tempo['FRAME'] == frame + i]

        if frame_apos['TIME_POSSE'].values == time2 and frame_apos['X'].values <= 110:
            return {frame: 'Bloqueado'}
        
        if frame_cruzamento['Y'].values >= 38:
            if frame_desfecho['Y'].values <= 18:
                return {frame: 'Perdido'}
            
            elif frame_desfecho['X'].values >= 112:
                seg_anterior = df_tempo[df_tempo['FRAME'] == frame - 25]
                if seg_anterior['TIME_POSSE'].values == time2 and frame_apos['X'].values <= 110:
                    return {frame: 'Bloqueado'}
                else:
                    return {frame: 'Perdido'}
            
            elif frame_desfecho['TIME_POSSE'].values == time2:
                return {frame: 'Bloqueado'}
            elif frame_desfecho['TIME_POSSE'].values == time1:
                return {frame: 'Bem-Sucedido'}
        
        elif frame_cruzamento['Y'].values < 38:
            if frame_desfecho['Y'].values >= 48:
                return {frame: 'Perdido'}
            
            elif frame_desfecho['X'].values >= 112:
                seg_anterior = df_tempo[df_tempo['FRAME'] == frame - 25]
                if seg_anterior['TIME_POSSE'].values == time2 and frame_apos['X'].values <= 110:
                    return {frame: 'Bloqueado'}
                else:
                    return {frame: 'Perdido'}
            
            elif frame_desfecho['TIME_POSSE'].values == time2:
                return {frame: 'Bloqueado'}
            elif frame_desfecho['TIME_POSSE'].values == time1:
                return {frame: 'Bem-Sucedido'}

# Função para obter os jogadores do time atacando
def obter_jogadores_atacando(df, frame, df_jogadores, lado_ataque):
    participantes = []

    # Localiza a posição da bola no frame desejado
    df_bola = df_jogadores[(df_jogadores['OBJETO_OBSERVADO'] == 'bola') & (df_jogadores['FRAME'] == frame)]
    x_bola = df_bola['X'].iloc[0]

    # Filtra os jogadores no frame e na faixa de tempo desejada
    df_frame_jogadores = df_jogadores[(df_jogadores['FRAME'] >= frame) & (df_jogadores['FRAME'] <= frame + 50) & (df_jogadores['OBJETO_OBSERVADO'] == 'jogador')]

    # Determina a área com base no lado de ataque
    if lado_ataque == 'DIREITA':
        area_ataque = (df_frame_jogadores["X"] > 101.5) & (df_frame_jogadores["Y"] > 17.85) & (df_frame_jogadores["Y"] < 58.15)
    elif lado_ataque == 'ESQUERDA':
        area_ataque = (df_frame_jogadores["X"] < 16.5) & (df_frame_jogadores["Y"] > 17.85) & (df_frame_jogadores["Y"] < 58.15)

    # Filtra os jogadores atacando
    df_jogadores_ataque = df_frame_jogadores[area_ataque]

    # Obtém os nomes dos jogadores atacando
    nomes_jogadores = df_jogadores_ataque['NOME_JOGADOR'].unique().tolist()

    # Atualiza a lista de participantes
    participantes = nomes_jogadores

    return participantes

# Função para obter os jogadores do outro time que estão defendendo
def obter_jogadores_defendendo(df, frame, df_jogadores, lado_ataque):
    participantes = []

    # Localiza a posição da bola no frame desejado
    df_bola = df_jogadores[(df_jogadores['OBJETO_OBSERVADO'] == 'bola') & (df_jogadores['FRAME'] == frame)]
    x_bola = df_bola['X'].iloc[0]

    # Filtra os jogadores no frame e na faixa de tempo desejada
    df_frame_jogadores = df_jogadores[(df_jogadores['FRAME'] >= frame) & (df_jogadores['FRAME'] <= frame + 50) & (df_jogadores['OBJETO_OBSERVADO'] == 'jogador')]

    # Determina a área com base no lado de ataque
    if lado_ataque == 'DIREITA':
        area_defesa = (df_frame_jogadores["X"] < 16.5) | ((df_frame_jogadores["X"] > 31.5) & (df_frame_jogadores["Y"] < 17.85) | (df_frame_jogadores["Y"] > 58.15))
    elif lado_ataque == 'ESQUERDA':
        area_defesa = (df_frame_jogadores["X"] > 101.5) | ((df_frame_jogadores["X"] < 86.5) & (df_frame_jogadores["Y"] < 17.85) | (df_frame_jogadores["Y"] > 58.15))

    # Filtra os jogadores defendendo
    df_jogadores_defesa = df_frame_jogadores[area_defesa]

    # Obtém os nomes dos jogadores defendendo
    nomes_jogadores = df_jogadores_defesa['NOME_JOGADOR'].unique().tolist()

    # Atualiza a lista de participantes
    participantes = nomes_jogadores

    return participantes

# Função para a análise de cruzamentos
def cruzamentos(df, id_time, tempo_jogo, times):
    resultados = {}

    # Identifica os times
    times = obtem_times(df)

    # Criação das colunas para indicar se a bola está dentro da área
    df_bola = df[df['OBJETO_OBSERVADO'] == 'bola']
    df_bola = colunas_bola_dentro_das_areas(df_bola)

    # Identifica o lado inicial do ataque
    lado_ataque = identifica_lado_do_ataque(df, id_time, tempo_jogo)

    # Define as zonas do campo
    zonas = definir_zonas(lado_ataque)

    # Análise inicial de cruzamentos
    if lado_ataque == 'DIREITA':
        df_ = df_bola[
            (df_bola['TIME_POSSE'] == id_time) &
            (df_bola['TEMPO_JOGO'] == tempo_jogo) &
            (df_bola['VELOCIDADE'] >= 1.5) &
            (df_bola['X'] < 118) &
            (df_bola['X'] >= 86.5) &
            (df_bola['Y'] < 75)
        ]
        df_.reset_index(drop=True, inplace=True)

    elif lado_ataque == 'ESQUERDA':
        df_ = df_bola[
            (df_bola['TIME_POSSE'] == id_time) &
            (df_bola['TEMPO_JOGO'] == tempo_jogo) &
            (df_bola['VELOCIDADE'] >= 1.5) &
            (df_bola['X'] > 0) &
            (df_bola['X'] <= 31.5) &
            (df_bola['Y'] < 75)
        ]
        df_.reset_index(drop=True, inplace=True)
    
    contador, frames_teste = primeira_analise_cruzamentos(df_bola, df_, zonas, lado_ataque, f'DENTRO_AREA_{lado_ataque}', duracao_lim=20)

    # Análise final de cruzamentos
    if id_time == times[0]:
        df_ =  df[df['TIME_JOGADOR'] != times[1]]
        df_jogadores = df_[df_['TEMPO_JOGO'] == tempo_jogo]
        
    elif id_time == times[1]:
        df_ =  df[df['TIME_JOGADOR'] != times[0]]
        df_jogadores = df_[df_['TEMPO_JOGO'] == tempo_jogo]
    
    cruzamentos_finais, frames_finais, jogadores_cruzaram, velocidades_maximas, zonas_ = analise_final_cruzamentos(df_bola, df_jogadores, zonas, frames_teste, lado_ataque, duracao_lim=20, distancia_lim=4)

    if id_time == times[0] == 'PAL':
    # Armazena os resultados
        resultados['time'] = {
            '1': {
                'id': 1,
                'nome': "Palmeiras",
                'liga': "Brasileirão Série A",
                'logo': "https://api.deltagoal.ai/1/logo.png",
                'rupturas': []
            }
        }

    elif id_time == times[1] == 'RED':
        resultados['time'] = {
            '5': {
                'id': 5,
                'nome': "Red Bull Bragantino",
                'liga': "Brasileirão Série A",
                'logo': "https://api.deltagoal.ai/5/logo.png",
                'rupturas': []
            }
        }

    if id_time == times[0]:
        df_ =  df[df['TIME_JOGADOR'] != times[1]]
        df_jogadores_ataque = df_[df_['TEMPO_JOGO'] == tempo_jogo]
        df__ =  df[df['TIME_JOGADOR'] != times[0]]
        df_jogadores_defesa = df__[df__['TEMPO_JOGO'] == tempo_jogo]
        
    elif id_time == times[1]:
        df_ =  df[df['TIME_JOGADOR'] != times[0]]
        df_jogadores_ataque = df_[df_['TEMPO_JOGO'] == tempo_jogo]
        df__ =  df[df['TIME_JOGADOR'] != times[1]]
        df_jogadores_defesa = df__[df__['TEMPO_JOGO'] == tempo_jogo]

    for idx, frame in enumerate(frames_finais):
        jogadores_atacando = obter_jogadores_atacando(df, frame, df_jogadores_ataque, lado_ataque)
        jogadores_defendendo = obter_jogadores_defendendo(df, frame, df_jogadores_defesa, lado_ataque)

        # Obtenha o desfecho do cruzamento
        desfecho_cruzamento = obter_desfecho_cruzamentos(df, frame, id_time, times, tempo_jogo)

        # Converta para um objeto timedelta
        delta_time = pd.to_timedelta(frame * 40, unit='ms')

        # Use strftime para formatar a hora sem os milissegundos
        instante_cruzamento = f"{delta_time.components.hours:02d}:{delta_time.components.minutes:02d}:{delta_time.components.seconds:02d}"
        
        cruzamento_info = {
            'instante_cruzamento': instante_cruzamento,
            'numero_jogadores_time_cruzando': [],
            'nome_jogadores_time_cruzando': jogadores_atacando,
            'quantidade_jogadores_time_atacando': len(jogadores_atacando),
            'numero_jogadores_time_defendendo': [],
            'nome_jogadores_time_defendendo': jogadores_defendendo,
            'quantidade_jogadores_defendendo': len(jogadores_defendendo),
            'desfecho': desfecho_cruzamento[frame],
            'zona': zonas_[idx],
        }

        if id_time == times[0] == 'PAL':
            resultados['time']['1']['rupturas'].append(cruzamento_info)

        elif id_time == times[1] == 'RED':
            resultados['time']['5']['rupturas'].append(cruzamento_info)

    return resultados