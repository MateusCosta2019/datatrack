# from numpy import record


# avatar = session['username'][0]
#     # ====================== exibe conexoes do usuario ==================================
#     id_user = session['id']
#     cursor = mysqldata.connection.cursor(MySQLdb.cursors.DictCursor)
#     cursor.execute(f'SELECT nome_conexao FROM conexoes WHERE table1_id_user = {id_user}')
#     dados = cursor.fetchall()
#     nomecon = []
#     if dados:
#         for row in dados:
#             nomecon.append(row['nome_conexao'])
            
#     else:
#         info = 'Você não possui nenhuma fonte de dados'
#     # ====================== exibe conexoes do usuario ==================================


#     # ====================== carrega base de tamplates ==================================
#     msg=''
#     cursor = mysqldata.connection.cursor(MySQLdb.cursors.DictCursor)
#     cursor.execute('SELECT id_taplate, nome_tamplate, url, imagem, descricao, tipo FROM tamplates WHERE tipo = "Vendas"')
#     records = cursor.fetchall()
#     if records == None:
#         msg = 'Erro ao carregar nossos tamplates, tente novamente dentro de alguns minutos ou entre em contato com nosso suporte.'
#     # ====================== carrega base de tamplates ==================================
    
#     # return render_template('tamplates_vendas.html', msg=msg, nomecon=nomecon, records=records, avatar=avatar)

from ast import Pass
from fileinput import filename
import os 
from conecta_db import conecta_db
import logging 
from datetime import datetime

connection = conecta_db()
cursor = connection.cursor()

def tamplate(nome_tamplate):
    msg = ''
    query = (f'SELECT ID FROM tbd_tamplates WHERE NOME_TAMPLATE = "{nome_tamplate}"')
    cursor.execute(query)
    resultador = cursor.fetchone()

    # idconn = resultador['id_conexao']
    idtamplate = resultador['ID']
    print(idtamplate)

