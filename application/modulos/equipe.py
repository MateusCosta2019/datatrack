import autho_mysql
import mysql.connector

host = autho_mysql.host
user = autho_mysql.user
password = autho_mysql.password
db = autho_mysql.database

# Intialize MySQL
conn = mysql.connector.connect(host=host, user=user, password=password, db=db)
cursor = conn.cursor()

def add_membro_equipe(email,id_use):
    query_email = "SELECT id_user FROM db_user WHERE email = '{e_mail}'".format(e_mail=email)
    cursor.execute(query_email)
    resultado = cursor.fetchone()
    id = resultado[0]
    aviso = ''
    if resultado:
        try:
            query = "INSERT INTO equipe (membro, responsavel) VALUES({resultado}, {id})".format(resultado=id, id=id_use)
            cursor.execute(query)
            conn.commit()
            aviso = 'Membro adicionado a sua lista.'
        except:
            aviso = 'Não foi possivel adicionar usuario a sua base de equipe'
    else:
        aviso = 'Não encontramos este email em nossa base de dados, verifique e tente novamente.'
    return aviso

def exluir_membro_equipe(email, id_user):
    query_email = "SELECT id_user FROM db_user WHERE email = '{e_mail}'".format(e_mail=email)
    cursor.execute(query_email)
    resultado = cursor.fetchone()
    id = resultado[0]
    print (id)
    aviso = ''

    try:
        query = "DELETE FROM equipe WHERE membro = {resultado} AND responsavel = {id_user}".format(resultado=id, id_user=id_user)
        cursor.execute(query)
        conn.commit()
        aviso = 'membro deletado com sucesso'
    except:
        aviso = 'não foi possivel deletar este membro, tente novamente.'

    return aviso
