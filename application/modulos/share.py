from numpy import insert
from conecta_db import conecta_db
import logging 
from datetime import datetime
import string
import random

connection = conecta_db()
cursor = connection.cursor()
def share_report():
    urlbase= 'http://localhost:8080/facebookinsights/Bk1qJsdOdLmarYiutbOKAzYxH8gs2SnAivZfJSGTOrwHqLPGv6'
    cursor.execute(f'SELECT ID FROM tbd_salvos WHERE URL = "{urlbase}"')
    resultador = cursor.fetchone()
    idtamplate = resultador[0]

    email_share = 't1304mts@prestadorcbmp.com.br'

    # seleciona id do usuario compartilhado
    cursor.execute(f'SELECT ID FROM tbd_usuario WHERE email = "{email_share}"')
    resultador = cursor.fetchone()
    # insere na base de dados compartilhada
    cursor.execute(f'SELECT NOME_DASHBOARD, URL, ID_CONEXAO FROM tbd_salvos WHERE URL = "{urlbase}"')

    
    print(idtamplate)
share_report()