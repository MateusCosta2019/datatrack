from modulos.conecta_db import conecta_db

connection = conecta_db()
cursor = connection.cursor()

def dashboard_geral(id_user):
    cursor.execute(f"""SELECT 
                        tbd_salvos.NOME_DASHBOARD, 
                        tbd_salvos.URL, 
                        DATA_CRIACAO 
                    FROM tbd_salvos 
                    WHERE ID_USUARIO = {id_user}""")

    dados = cursor.fetchall()
    resultado = dados[0]
    return resultado
    
# dashboard_geral(id_user=11)
