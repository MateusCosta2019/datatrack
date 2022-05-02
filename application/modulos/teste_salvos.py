from conecta_db import conecta_db
import logging 
from datetime import datetime
import string
import random

connection = conecta_db()
cursor = connection.cursor()

def chaveurl():
    cursor.execute(f'SELECT URL FROM tbd_tamplates WHERE NOME_TAMPLATE = "Facebook Insights"')
    resultador = cursor.fetchone()
    url_base = resultador[0]
    
    # cursor.execute(f'SELECT URL FROM tbd_tamplates WHERE NOME_TAMPLATE = "Facebook Insights"')
    # resultador = cursor.fetchone()
    # idtamplate = resultador[0]
    # # cursor.execute('INSERT INTO tbd_salvos (NOME_DASHBOARD, ID_USUARIO, ID_TAMPLATES, ID_CONEXAO) VALUES (%s,%s,%s,%s)', (nome_dash,user, idtamplate, "1"))
    # # cursor.commit()
    escolhas_possiveis = string.ascii_letters + string.digits
    resultado = ''
    for i in range(50):
      resultado += random.choice(escolhas_possiveis)
    novo_url = url_base+'/'+resultado
    chave_unica = novo_url[39:]
    print(novo_url)

    # print(url_base)




chaveurl()