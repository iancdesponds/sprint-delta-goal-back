from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_pymongo import PyMongo
from credentials import settings, credenciais, secret_jwt
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import os
import re
import jwt
from utils import verifica_session
from analise_de_dados.data_cruzamentos import (
    df_pal,
    df_red,
    df_destaques_pal,
    df_destaques_red,
    zonas_cuzamentos_pal,
    zonas_cuzamentos_red,
    quant_desfechos_cruzamentos_pal,
    quant_desfechos_cruzamentos_red,
)
from analise_de_dados.data_quebra_linha import (
    data,
    df_ql_pal,
    df_ql_red,
    df_destaques_ql_pal,
    df_destaques_ql_red,
)
from quebra_de_linha_pal import desfechos_pal
from quebra_de_linha_red import desfechos_red

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

@app.route("/", methods=["GET"])
def home():
    return "<h1>Home Page - API</h1>", 200


@app.route("/login", methods=["POST"])
def login():
    try:
        if request.method == "POST":
            email = request.json.get("email")
            senha = request.json.get("senha")

            if not email or not senha:
                return "Credenciais incompletas", 400

            users = mongo.db.users
            user = users.find_one({"email": email})

            if user and bcrypt.check_password_hash(user["senha"], senha):
                nome = user["nome"]
                session = jwt.encode(
                    {"email": email, "nome": nome}, secret_jwt, algorithm="HS256"
                )
                mongo_session = mongo.db.sessions
                existe_session = mongo_session.find_one({"session": session})
                if existe_session == None:
                    mongo_session.insert_one({"session": session})

                return (
                    jsonify(
                        {
                            "message": "Login realizado com sucesso!",
                            "ok": True,
                            "session": session,
                        }
                    ),
                    200,
                )
            else:
                return (
                    jsonify(
                        {
                            "message": "E-mail ou senha incorretos. Tente novamente!",
                            "ok": False,
                        }
                    ),
                    404,
                )
    except Exception as e:
        return str(e), 500


@app.route("/register", methods=["POST"])
def register():
    try:
        if request.method == "POST":
            nome = request.json.get("nome")
            email = request.json.get("email")
            senha = request.json.get("senha")
            confirma_senha = request.json.get("confirma_senha")

            error_message = ""
            if len(senha) < 8 or not re.search(r"\d", senha):
                error_message = "A senha deve ter pelo menos 8 caracteres e incluir pelo menos um número."
            elif senha != confirma_senha:
                error_message = "As senhas não coincidem"
            elif mongo.db.users.find_one({"email": email}):
                error_message = "E-mail já cadastrado"
            if not nome or not email or not senha or not confirma_senha:
                return "Credenciais incompletas", 400
            users = mongo.db.users
            existing_user = users.find_one({"email": email})

            if existing_user:
                return "Usuário já existe!", 400

            hashed_password = bcrypt.generate_password_hash(senha)
            users.insert_one({"nome": nome, "email": email, "senha": hashed_password})
            return "Usuário registrado com sucesso!", 201
    except Exception as e:
        return str(e), 500


@app.route("/logout", methods=["DELETE"])
def logout():
    session = request.headers.get("Authorization")[7:]
    mongo_session = mongo.db.sessions
    mongo_session.delete_one({"session": session})
    return jsonify({"message": "Logout realizado com sucesso!", "ok": True}), 200


@app.route("/cruzamentos", methods=["GET", "POST"])
def cruzamentos():
    if request.method == "GET":
        df_cruzametos = {
            "pal": df_pal.to_dict("records"),
            "red": df_red.to_dict("records"),
        }
        return jsonify({"cruzamentos": df_cruzametos, "ok": True}), 200


@app.route("/cruzamentos/destaques", methods=["GET"])
def destaques_cruzamentos():
    if request.method == "GET":
        destaques = {
            "pal": df_destaques_pal.to_dict("records"),
            "red": df_destaques_red.to_dict("records"),
        }
        return jsonify({"destaques": destaques, "ok": True}), 200
    else:
        return jsonify({"message": "Método não permitido"}), 405


@app.route("/cruzamentos/desfechos", methods=["GET"])
def desfechos_cruzamentos():
    if request.method == "GET":
        desfechos = {
            "pal": quant_desfechos_cruzamentos_pal,
            "red": quant_desfechos_cruzamentos_red,
        }
        return jsonify({"desfechos": desfechos, "ok": True}), 200
    else:
        return jsonify({"message": "Método não permitido"}), 405


@app.route("/cruzamentos/zonas", methods=["GET"])
def zonas_cruzamentos():
    if request.method == "GET":
        zonas_porcentagens = {"pal": zonas_cuzamentos_pal, "red": zonas_cuzamentos_red}
        return jsonify({"zonas": zonas_porcentagens, "ok": True}), 200
    else:
        return jsonify({"message": "Método não permitido"}), 405
    
@app.route("/cruzamentos/geral", methods=["GET"])
def geral_cruzamentos():
    if request.method == "GET":
        zonas_porcentagens = {"pal": zonas_cuzamentos_pal, "red": zonas_cuzamentos_red}

        desfechos = {
                "pal": quant_desfechos_cruzamentos_pal,
                "red": quant_desfechos_cruzamentos_red,
            }
        
        destaques = {
                "pal": df_destaques_pal.to_dict("records"),
                "red": df_destaques_red.to_dict("records"),
            }

        df_cruzametos = {
                "pal": df_pal.to_dict("records"),
                "red": df_red.to_dict("records"),
            }
        
        return jsonify({"zonas": zonas_porcentagens, "desfechos": desfechos, "destaques": destaques, "cruzamentos": df_cruzametos, "ok": True}), 200

@app.route("/quebra_linha", methods=["GET", "POST"])
def quebra_linha():
    if request.method == "GET":
        quebra_linha = {
            "pal": df_ql_pal.to_dict("records"),
            "red": df_ql_red.to_dict("records"),
        }
        return jsonify({"quebras_linha": quebra_linha, "rupturas":data, "ok": True}), 200


@app.route("/quebra_linha/destaques", methods=["GET"])
def destaques_quebra_linha():
    if request.method == "GET":
        destaques = {
            "pal": df_destaques_ql_pal.to_dict("records"),
            "red": df_destaques_ql_red.to_dict("records"),
        }
        return jsonify({"destaques": destaques, "ok": True}), 200
    else:
        return jsonify({"message": "Método não permitido"}), 405

@app.route("/modelo_quebra_linha/geral", methods=["GET"])
def modelo_quebra_linha():
    if request.method == "GET":
        quebra_linha_json = partidas.find_one({"nome": "modelo_quebra_linha"})
        quebra_linha_json['_id'] = ''
        return quebra_linha_json, 200
    else:
        return jsonify({"message": "Método não permitido"}), 405

@app.route("/palmeiras_desfechos")
def desfechos_palmeiras():
    return desfechos_pal

@app.route("/bragantino_desfechos")
def desfechos_bragantino():
    return desfechos_red

if __name__ == "__main__":
    app.run(debug=True, port=5000)
