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

def dash_compratilhados():
    cursor.execute(f'SELECT ID_TAMPLATE FROM tbd_compartilhados WHERE ID_USUARIO_COMP = 19;')
    ID_TAMPLATE = cursor.fetchone()
    ID_TAMPLATE = ID_TAMPLATE[0]
    cursor.execute(f'SELECT NOME_DASHBOARD, THUMBNAIL, URL FROM tbd_salvos INNER JOIN tbd_tamplates ON tbd_tamplates.ID = tbd_salvos.ID WHERE ID_TAMPLATES = {ID_TAMPLATE}')
    DADOS_DASHBOARD = cursor.fetchall()


def compartilha():
    email = 't1304mts@prestadorcbmp.com.br'
    id = 1
    id_tamplate_ = 1
    cursor.execute(f'SELECT ID FROM tbd_usuario WHERE EMAIL = "{email}"')
    id_user = cursor.fetchone()
    id_user_ = id_user[0]
    cursor.execute('INSERT INTO tbd_compartilhados (ID_USUARIO_CRIADOR, ID_USUARIO_COMP, ID_TAMPLATE) VALUES (%s, %s, %s);', (id, id_user_, id_tamplate_))
    connection.commit()


# def cadastro():
#     cursor.execute(f'SELECT URL FROM tbd_tamplates WHERE NOME_TAMPLATE = "Facebook Insights"')
#     resultador = cursor.fetchone()
#     idtamplate = resultador['ID']
#     # cursor.execute('INSERT INTO tbd_salvos (NOME_DASHBOARD, ID_USUARIO, ID_TAMPLATES, ID_CONEXAO) VALUES (%s,%s,%s,%s)', (nome_dash,user, idtamplate, "1"))
#     # cursor.commit()
#     print(idtamplate)
    
# cadastro()