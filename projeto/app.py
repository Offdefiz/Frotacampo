import json
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from datetime import datetime, timedelta
from bcrypt import hashpw, gensalt, checkpw
from bcrypt import hashpw, gensalt
import pandas as pd
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pandas as pd
import json

senha = "senha123"  # Substitua pela senha desejada
hashed = hashpw(senha.encode("utf-8"), gensalt())
print(hashed.decode("utf-8"))

app = Flask(__name__)
app.secret_key = "sua_chave_secreta" # Substitua por uma chave segura em produção

# Tradução de dias da semana
dias_semana_pt_br = {
    "Monday": "Segunda-feira",
    "Tuesday": "Terça-feira",
    "Wednesday": "Quarta-feira",
    "Thursday": "Quinta-feira",
    "Friday": "Sexta-feira",
    "Saturday": "Sábado",
    "Sunday": "Domingo"
}

# Carregar dados de arquivos JSON

try:
    with open("estados.json", "r", encoding="utf-8") as f:
        estados = json.load(f)
except FileNotFoundError:
    estados = {}
try:
    with open("rotas.json", "r", encoding="utf-8") as f:
        rotas = json.load(f)
except FileNotFoundError:
    rotas = {}
with open("usuarios.json", "r", encoding="utf-8") as f:
    usuarios = json.load(f)
try:
    with open("dados.json", "r", encoding="utf-8") as f:
        dados = json.load(f)
except FileNotFoundError:
    dados = {}

# Caminhos dos arquivos
json_path = "dados.json"
excel_path = "planilha.xlsx"

# Função para processar o JSON e atualizar a planilha
def atualizar_planilha():
    try:
        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        registros = []
        for email, items in data.items():
            for item in items:
                item["E-mail Principal"] = email
                registros.append(item)

        df = pd.DataFrame(registros)
        with pd.ExcelWriter(excel_path, mode="w", engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Dados Consolidado")
        
        print("Planilha atualizada com sucesso!")
    except Exception as e:
        print(f"Erro ao atualizar a planilha: {e}")



# Funções auxiliares
def adicionar_dias_uteis(data, dias_uteis):
    dias_adicionados = 0
    while dias_adicionados < dias_uteis:
        data += timedelta(days=1)
        if data.weekday() < 5:  # Segunda a Sexta
            dias_adicionados += 1
    return data

def proximo_dia_entrega(data_inicial, dias_entrega):
    dias_indices = {
        "Segunda": 0, "Terça": 1, "Quarta": 2, "Quinta": 3, "Sexta": 4
    }
    entrega_indices = [dias_indices[dia] for dia in dias_entrega]
    for _ in range(7):
        if data_inicial.weekday() in entrega_indices:
            return data_inicial
        data_inicial += timedelta(days=1)
    return None

# Rotas
@app.route("/")
def home():
    if not session.get("logged_in"):
        print("Usuário não está logado.")  # Debug
        return redirect(url_for("login"))
    print("Usuário logado: ", session.get("user"))  # Debug
    return render_template("index.html", estados=estados)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    data = request.form
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"success": False, "message": "E-mail e senha são obrigatórios."}), 400

    # Verificar se o e-mail existe no arquivo JSON
    for user in usuarios:
        if user["email"] == email:
            # Validar senha com bcrypt
            if checkpw(password.encode("utf-8"), user["password"].encode("utf-8")):
                session["logged_in"] = True
                session["user"] = email
                return redirect(url_for("home"))

            return jsonify({"success": False, "message": "Senha incorreta."}), 401

    return jsonify({"success": False, "message": "E-mail não encontrado."}), 404


@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()  # Limpa a sessão
    session["logged_in"] = True
    return render_template("login.html")  # Redireciona para a página de login

@app.route("/signup", methods=["POST"])
def signup():
    data = request.form
    email = data.get("email")
    password = data.get("password")
    username = data.get("username")
    
    # Carregar usuários existentes
    try:
        with open("usuarios.json", "r", encoding="utf-8") as f:
            usuarios = json.load(f)
    except FileNotFoundError:
        usuarios = []

    # Verificar se o e-mail já existe
    for user in usuarios:
        if user["email"] == email:
            return jsonify({"success": False, "message": "E-mail já cadastrado."}), 400

    # Criar hash da senha
    hashed_password = hashpw(password.encode("utf-8"), gensalt())

    # Adicionar novo usuário
    usuarios.append({
        "email": email,
        "password": hashed_password.decode("utf-8"),
        "username": username,
        
    })

    # Salvar no arquivo
    with open("usuarios.json", "w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=4, ensure_ascii=False)
    return redirect(url_for("login"))

@app.route("/calculate", methods=["POST"])
def calculate():
    # Verificar se o usuário está logado
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    # Carregar histórico
    try:
        with open("historico.json", "r", encoding="utf-8") as f:
            historico = json.load(f)
    except FileNotFoundError:
        historico = {}

    # Dados do cálculo
    data = request.json
    estado = data.get("estado")
    cidade = data.get("cidade")
    volume = float(data.get("volume", 0))
    data_faturamento = datetime.strptime(data.get("data_faturamento"), "%Y-%m-%d")

    if cidade not in rotas:
        return jsonify({"error": "Cidade não encontrada na lista de rotas."})
    if volume < 30:
        return jsonify({"error": "Volume insuficiente para envio."})
    elif volume > 500:
        return jsonify({"error": "Volume excede o limite para envio automático. Consulte a logística."})

    dias_uteis = rotas[cidade]["dias_uteis"]
    dias_entrega = rotas[cidade]["dias_entrega"]

    # Calcular data de entrega
    data_entrega_inicial = adicionar_dias_uteis(data_faturamento, dias_uteis)
    data_entrega_final = proximo_dia_entrega(data_entrega_inicial, dias_entrega)

    if data_entrega_final:
        dia_semana = data_entrega_final.strftime("%A")
        dia_semana_pt_br = dias_semana_pt_br.get(dia_semana, dia_semana)
        data_formatada = data_entrega_final.strftime("%d/%m/%Y")

        # Atualizar histórico
        user_email = session["user"]
        if user_email not in historico:
            historico[user_email] = []

        historico[user_email].append({
            "estado": estado,
            "cidade": cidade,
            "volume": volume,
            "data_faturamento": data.get("data_faturamento"),
            "data_entrega": data_formatada
        })

        # Salvar histórico no arquivo
        with open("historico.json", "w", encoding="utf-8") as f:
            json.dump(historico, f, indent=4, ensure_ascii=False)

        return jsonify({"dia_semana": dia_semana_pt_br, "data": data_formatada})
    else:
        return jsonify({"error": "Não há datas de entrega disponíveis."})
    
@app.route("/cadastro", methods=["GET"])
def cadastroCliente():
    if session.get("logged_in"):
         return render_template("cadastro.html")

@app.route("/registrar_cliente", methods=["POST"])
def registrar_cliente():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    # Receber os dados enviados pelo formulário
    novo_cliente = request.json
    email = novo_cliente.get("email")

    # Validar se o e-mail foi enviado
    if not email:
        return jsonify({"error": "E-mail é obrigatório"}), 400

    # Carregar os dados existentes
    try:
        with open("dados.json", "r", encoding="utf-8") as f:
            dados = json.load(f)
    except FileNotFoundError:
        dados = {}

    # Adicionar o cliente ao e-mail correspondente
    if email not in dados:
        dados[email] = []

    dados[email].append({
        "VENDEDOR": novo_cliente.get("vendedor"),
        "Razão Social": novo_cliente.get("razao_social"),
        "CNPJ": novo_cliente.get("cnpj"),
        "Endereço com CEP": novo_cliente.get("endereco"),
        "E-mail": novo_cliente.get("email"),
        "Telefone": novo_cliente.get("telefone"),
        "Data de Envio ao Assistente": novo_cliente.get("data_envio"),
        "Logistica": novo_cliente.get("logistica")
    })

    # Atualizar a planilha
    atualizar_planilha()

    # Salvar os dados atualizados no arquivo JSON
    with open("dados.json", "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

    return jsonify({"message": "Cliente registrado com sucesso!"}), 200

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
    