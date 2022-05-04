from modulos.conecta_db import conecta_db
import string
import random

connection = conecta_db()
cursor = connection.cursor()

def gera_chave():
    escolhas_possiveis = string.ascii_letters + string.digits
    resultado = ''
    for i in range(8):
        resultado += random.choice(escolhas_possiveis)
   
    return resultado

def reset_password(email, senha):
    """
    Para a função de recuperação de senha deve ser passado 3 parametros para prosseguir:
        nome
        sobrenome
        email
    
    após passados a função ira realizar a alteração da senha
    """

    email = email
    senha = senha
    retorno = ''


    # seleciona o id do usuario para atualiza senha
    query_select = f'SELECT ID FROM tbd_usuario WHERE email = "{email}"'
    cursor.execute(query_select)
    query_select = cursor.fetchone()
    
    if query_select == None:
        retorno = 'Nenhum usuario com o email'

    else:
        id = int(query_select[0])
   
        # troca senha do usuarioMD5(%s)
        update = f'UPDATE tbd_usuario set SENHA=MD5("{senha}") where ID={id}'
        cursor.execute(update)
        connection.commit()
        retorno = 'Alteração bem suscedida'

    return retorno

# reset_password(email='mateus@tellusgestao.com.br', senha='alfa1204')

