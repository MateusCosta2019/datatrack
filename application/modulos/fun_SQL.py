from ast import Pass
from fileinput import filename
import os 
from modulos.conecta_db import conecta_db
import logging 
from datetime import datetime

connection = conecta_db()
cursor = connection.cursor()

def cadastro(nome, sobrenome, email, senha):

    # def verifica_cadastro():
    #     cursor.execute('SELECT EMAIL FROM tbd_usuario WHERE EMAIL = %s',(email))
    
    # if verifica_cadastro == True:
    #     err = 'Email já cadastrado no nosso sistema, faça login com o email e senha'
    try:
        query = ''
        query = cursor.execute('INSERT INTO tbd_usuario (NOME, SOBRENOME, EMAIL, SENHA) VALUES (%s, %s, %s, md5(%s))', (nome, sobrenome, email, senha))
        connection.commit()
        print('Usuário cadastrado com sucesso!')
    except Exception as erro:
        logging.error(f'Não Foi possivel executar a query {query}. Erro:', erro)
        exit()

def conexoes(id):
    cursor.execute(f'SELECT ID, NOME_CONEXAO FROM tbd_conexoes WHERE ID_USUARIO = {id}')
    dados = cursor.fetchall()
    return dados

    
def cadastro_adm(nome, sobrenome, email):

    # def verifica_cadastro():
    #     cursor.execute('SELECT EMAIL FROM tbd_usuario WHERE EMAIL = %s',(email))
    
    # if verifica_cadastro == True:
    #     err = 'Email já cadastrado no nosso sistema, faça login com o email e senha'

    cursor.execute(f'SELECT EMPRESA FROM tbd_usuario WHERE ID=11')
    empresa_usuario = cursor.fetchone()
    ano = str(datetime.now().strftime('%Y'))
    senha = empresa_usuario[0] + '_' + ano

    try:
        cursor.execute('INSERT INTO tbd_usuario (NOME, SOBRENOME, EMAIL, EMPRESA, SENHA) VALUES (%s, %s, %s, %s, md5(%s))', (nome, sobrenome, email, empresa_usuario[0], senha))
        connection.commit()
        print('Usuário cadastrado com sucesso!')
    except Exception as erro:
        logging.error(f'Não Foi possivel executar a query, Erro:', erro)
        exit()


def mostra_equipe(id):
    cursor.execute(f'SELECT EMPRESA FROM tbd_usuario WHERE ID={id}')
    empresa_usuario = cursor.fetchone()
    empresa = empresa_usuario[0]

    return empresa
