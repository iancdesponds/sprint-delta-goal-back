import random


def token_generator():
    # Caracteres alfanuméricos seguros
    alfanumericos = (
        [chr(i) for i in range(65, 91)]
        + [chr(i) for i in range(97, 123)]
        + [chr(i) for i in range(48, 58)]
    )

    # Caracteres especiais seguros
    caracteres_especiais = ["-", "_"]

    # Combinando todos os caracteres seguros
    caracteres_seguros = alfanumericos + caracteres_especiais

    token = ""
    n = len(caracteres_seguros) - 1
    size = 25

    for i in range(size):
        token += caracteres_seguros[random.randint(0, n)]

    return token


def verifica_session(session, collection):
    mongo_sessions = collection
    existe_session = mongo_sessions.find_one({"session": session})
    if existe_session == None or existe_session == "":
        return False
    else:
        return True
