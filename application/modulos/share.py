from numpy import insert
from conecta_db import conecta_db
import logging 
from datetime import datetime
import string
import random

connection = conecta_db()
cursor = connection.cursor()

def share_report(email_share, id_usuario, Url_base):
    email_share = 't1304mts@prestadorcbmp.com.br'

    # seleciona id do usuario compartilhado
    email=''
    cursor.execute(f'SELECT ID FROM tbd_usuario WHERE email = "{email_share}"')
    resultador = cursor.fetchone()
    email = resultador[0]


    # insere na base de dados compartilhada
    # cursor.execute(f'SELECT NOME_DASHBOARD, URL, ID_CONEXAO FROM tbd_salvos WHERE URL = "{urlbase}"')
    id_usuario = id_usuario
    cursor.execute('INSERT INTO tbd_compartilhados (ID_USUARIO_CRIADOR, ID_USUARIO_COMP, URL_BASE) VALUES (%s, %s, %s)', (id_usuario, email, Url_base))
    connection.commit()
    print('Compartilhado')

    
share_report(email_share='t1304mts@prestadorcbmp.com.br', id_usuario=11, Url_base='http://localhost:8080/facebookinsights/Bk1qJsdOdLmarYiutbOKAzYxH8gs2SnAivZfJSGTOrwHqLPGv6')