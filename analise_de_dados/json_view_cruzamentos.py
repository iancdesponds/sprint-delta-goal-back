from view_cruzamentos import *

# Criação do JSON completo:

df = dados(r'C:\Users\henri\Insper\sprints\sprint-2023.2\delta-goal-grupo-4\dados\dados_brutos.csv')

times = obtem_times(df)

resultados = {}

# Criação das colunas para indicar se a bola está dentro da área
df_bola = df[df['OBJETO_OBSERVADO'] == 'bola']
df_bola = colunas_bola_dentro_das_areas(df_bola)

times = ['PAL', 'RED']

# PALMEIRAS 1º TEMPO:

# Identifica o lado inicial do ataque
lado_ataque = identifica_lado_do_ataque(df, 'PAL', 1)

# Define as zonas do campo
zonas = definir_zonas(lado_ataque)

# Análise inicial de cruzamentos
if lado_ataque == 'DIREITA':
    df_ = df_bola[
        (df_bola['TIME_POSSE'] == 'PAL') &
        (df_bola['TEMPO_JOGO'] == 1) &
        (df_bola['VELOCIDADE'] >= 1.5) &
        (df_bola['X'] < 118) &
        (df_bola['X'] >= 86.5) &
        (df_bola['Y'] < 75)
    ]
    df_.reset_index(drop=True, inplace=True)

elif lado_ataque == 'ESQUERDA':
    df_ = df_bola[
        (df_bola['TIME_POSSE'] == 'PAL') &
        (df_bola['TEMPO_JOGO'] == 1) &
        (df_bola['VELOCIDADE'] >= 1.5) &
        (df_bola['X'] > 0) &
        (df_bola['X'] <= 31.5) &
        (df_bola['Y'] < 75)
    ]
    df_.reset_index(drop=True, inplace=True)

contador, frames_teste = primeira_analise_cruzamentos(df_bola, df_, zonas, lado_ataque, f'DENTRO_AREA_{lado_ataque}', duracao_lim=20)

df_ =  df[df['TIME_JOGADOR'] != 'RED']
df_jogadores = df_[df_['TEMPO_JOGO'] == 1]

cruzamentos_finais, frames_finais, jogadores_cruzaram, velocidades_maximas, zonas_ = analise_final_cruzamentos(df_bola, df_jogadores, zonas, frames_teste, lado_ataque, duracao_lim=20, distancia_lim=4)

resultados['time'] = {
    '1': {
        'id': 1,
        'nome': "Palmeiras",
        'liga': "Brasileirão Série A",
        'logo': "https://api.deltagoal.ai/1/logo.png",
        'rupturas': []
    }
}

df_ =  df[df['TIME_JOGADOR'] != 'RED']
df_jogadores_ataque = df_[df_['TEMPO_JOGO'] == 1]
df__ =  df[df['TIME_JOGADOR'] != 'PAL']
df_jogadores_defesa = df__[df__['TEMPO_JOGO'] == 1]

for idx, frame in enumerate(frames_finais):
    jogadores_atacando = obter_jogadores_atacando(df, frame, df_jogadores_ataque, lado_ataque)
    jogadores_defendendo = obter_jogadores_defendendo(df, frame, df_jogadores_defesa, lado_ataque)

    # Obtenha o desfecho do cruzamento
    desfecho_cruzamento = obter_desfecho_cruzamentos(df, frame, 'PAL', times, 1)

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

    resultados['time']['1']['rupturas'].append(cruzamento_info)


# PALMEIRAS 2º TEMPO:

# Identifica o lado inicial do ataque
lado_ataque = identifica_lado_do_ataque(df, 'PAL', 2)

# Define as zonas do campo
zonas = definir_zonas(lado_ataque)

# Análise inicial de cruzamentos
if lado_ataque == 'DIREITA':
    df_ = df_bola[
        (df_bola['TIME_POSSE'] == 'PAL') &
        (df_bola['TEMPO_JOGO'] == 2) &
        (df_bola['VELOCIDADE'] >= 1.5) &
        (df_bola['X'] < 118) &
        (df_bola['X'] >= 86.5) &
        (df_bola['Y'] < 75)
    ]
    df_.reset_index(drop=True, inplace=True)

elif lado_ataque == 'ESQUERDA':
    df_ = df_bola[
        (df_bola['TIME_POSSE'] == 'PAL') &
        (df_bola['TEMPO_JOGO'] == 2) &
        (df_bola['VELOCIDADE'] >= 1.5) &
        (df_bola['X'] > 0) &
        (df_bola['X'] <= 31.5) &
        (df_bola['Y'] < 75)
    ]
    df_.reset_index(drop=True, inplace=True)

contador, frames_teste = primeira_analise_cruzamentos(df_bola, df_, zonas, lado_ataque, f'DENTRO_AREA_{lado_ataque}', duracao_lim=20)

df_ =  df[df['TIME_JOGADOR'] != 'RED']
df_jogadores = df_[df_['TEMPO_JOGO'] == 2]

cruzamentos_finais, frames_finais, jogadores_cruzaram, velocidades_maximas, zonas_ = analise_final_cruzamentos(df_bola, df_jogadores, zonas, frames_teste, lado_ataque, duracao_lim=20, distancia_lim=4)

df_ =  df[df['TIME_JOGADOR'] != 'RED']
df_jogadores_ataque = df_[df_['TEMPO_JOGO'] == 2]
df__ =  df[df['TIME_JOGADOR'] != 'PAL']
df_jogadores_defesa = df__[df__['TEMPO_JOGO'] == 2]

for idx, frame in enumerate(frames_finais):
    jogadores_atacando = obter_jogadores_atacando(df, frame, df_jogadores_ataque, lado_ataque)
    jogadores_defendendo = obter_jogadores_defendendo(df, frame, df_jogadores_defesa, lado_ataque)

    # Obtenha o desfecho do cruzamento
    desfecho_cruzamento = obter_desfecho_cruzamentos(df, frame, 'PAL', times, 2)

    # Converta para um objeto timedelta
    delta_time = pd.to_timedelta((frame+70725) * 40, unit='ms')

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

    resultados['time']['1']['rupturas'].append(cruzamento_info)


# RED BULL BRAGANTINO 1º TEMPO:

# Identifica o lado inicial do ataque
lado_ataque = identifica_lado_do_ataque(df, 'RED', 1)

# Define as zonas do campo
zonas = definir_zonas(lado_ataque)

# Análise inicial de cruzamentos
if lado_ataque == 'DIREITA':
    df_ = df_bola[
        (df_bola['TIME_POSSE'] == 'RED') &
        (df_bola['TEMPO_JOGO'] == 1) &
        (df_bola['VELOCIDADE'] >= 1.5) &
        (df_bola['X'] < 118) &
        (df_bola['X'] >= 86.5) &
        (df_bola['Y'] < 75)
    ]
    df_.reset_index(drop=True, inplace=True)

elif lado_ataque == 'ESQUERDA':
    df_ = df_bola[
        (df_bola['TIME_POSSE'] == 'RED') &
        (df_bola['TEMPO_JOGO'] == 1) &
        (df_bola['VELOCIDADE'] >= 1.5) &
        (df_bola['X'] > 0) &
        (df_bola['X'] <= 31.5) &
        (df_bola['Y'] < 75)
    ]
    df_.reset_index(drop=True, inplace=True)

contador, frames_teste = primeira_analise_cruzamentos(df_bola, df_, zonas, lado_ataque, f'DENTRO_AREA_{lado_ataque}', duracao_lim=20)

df_ =  df[df['TIME_JOGADOR'] != 'PAL']
df_jogadores = df_[df_['TEMPO_JOGO'] == 1]

cruzamentos_finais, frames_finais, jogadores_cruzaram, velocidades_maximas, zonas_ = analise_final_cruzamentos(df_bola, df_jogadores, zonas, frames_teste, lado_ataque, duracao_lim=20, distancia_lim=4)

resultados['time']['5'] = {
    'id': 5,
        'nome': "Red Bull Bragantino",
        'liga': "Brasileirão Série A",
        'logo': "https://api.deltagoal.ai/5/logo.png",
        'rupturas': []
    }

df_ =  df[df['TIME_JOGADOR'] != 'PAL']
df_jogadores_ataque = df_[df_['TEMPO_JOGO'] == 1]
df__ =  df[df['TIME_JOGADOR'] != 'RED']
df_jogadores_defesa = df__[df__['TEMPO_JOGO'] == 1]

for idx, frame in enumerate(frames_finais):
    jogadores_atacando = obter_jogadores_atacando(df, frame, df_jogadores_ataque, lado_ataque)
    jogadores_defendendo = obter_jogadores_defendendo(df, frame, df_jogadores_defesa, lado_ataque)

    # Obtenha o desfecho do cruzamento
    desfecho_cruzamento = obter_desfecho_cruzamentos(df, frame, 'RED', times, 1)

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

    resultados['time']['5']['rupturas'].append(cruzamento_info)

# RED BULL BRAGANTINO 2º TEMPO:

# Identifica o lado inicial do ataque
lado_ataque = identifica_lado_do_ataque(df, 'RED', 2)

# Define as zonas do campo
zonas = definir_zonas(lado_ataque)

# Análise inicial de cruzamentos
if lado_ataque == 'DIREITA':
    df_ = df_bola[
        (df_bola['TIME_POSSE'] == 'RED') &
        (df_bola['TEMPO_JOGO'] == 2) &
        (df_bola['VELOCIDADE'] >= 1.5) &
        (df_bola['X'] < 118) &
        (df_bola['X'] >= 86.5) &
        (df_bola['Y'] < 75)
    ]
    df_.reset_index(drop=True, inplace=True)

elif lado_ataque == 'ESQUERDA':
    df_ = df_bola[
        (df_bola['TIME_POSSE'] == 'RED') &
        (df_bola['TEMPO_JOGO'] == 2) &
        (df_bola['VELOCIDADE'] >= 1.5) &
        (df_bola['X'] > 0) &
        (df_bola['X'] <= 31.5) &
        (df_bola['Y'] < 75)
    ]
    df_.reset_index(drop=True, inplace=True)

contador, frames_teste = primeira_analise_cruzamentos(df_bola, df_, zonas, lado_ataque, f'DENTRO_AREA_{lado_ataque}', duracao_lim=20)

df_ =  df[df['TIME_JOGADOR'] != 'PAL']
df_jogadores = df_[df_['TEMPO_JOGO'] == 2]

cruzamentos_finais, frames_finais, jogadores_cruzaram, velocidades_maximas, zonas_ = analise_final_cruzamentos(df_bola, df_jogadores, zonas, frames_teste, lado_ataque, duracao_lim=20, distancia_lim=4)

df_ =  df[df['TIME_JOGADOR'] != 'PAL']
df_jogadores_ataque = df_[df_['TEMPO_JOGO'] == 2]
df__ =  df[df['TIME_JOGADOR'] != 'RED']
df_jogadores_defesa = df__[df__['TEMPO_JOGO'] == 2]

for idx, frame in enumerate(frames_finais):
    jogadores_atacando = obter_jogadores_atacando(df, frame, df_jogadores_ataque, lado_ataque)
    jogadores_defendendo = obter_jogadores_defendendo(df, frame, df_jogadores_defesa, lado_ataque)

    # Obtenha o desfecho do cruzamento
    desfecho_cruzamento = obter_desfecho_cruzamentos(df, frame, 'RED', times, 2)

    # Converta para um objeto timedelta
    delta_time = pd.to_timedelta((frame+70725) * 40, unit='ms')

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

    resultados['time']['5']['rupturas'].append(cruzamento_info)

import json
print(json.dumps(resultados, indent=4))