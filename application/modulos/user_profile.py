from modulos.conecta_db import conecta_db

connection = conecta_db()
cursor = connection.cursor()

def info(user_id):
    query = f"SELECT concat(NOME,' ',SOBRENOME) as NOME, EMAIL, TEL FROM tbd_usuario WHERE ID = {user_id}"
    cursor.execute(query)
    resultado = cursor.fetchall()

    nome = []
    email = [] 
    telefone = []

    for item in resultado:
        nome = item[0]
        email = item[1] 
        telefone = item[2]

    dados = {
        'Nome': nome,
        'Email': email,
        'Tel': telefone
    }

    return dados

print(profile(user_id=11))