from modulos.conecta_db import conecta_db

connection = conecta_db()
cursor = connection.cursor()

# delete dashboards from user page
def deleta_dashboard(id_user=int, nome_delete=str):
    cursor.execute('SELECT id FROM favoritos WHERE nome_dashboard = %s AND user_id_user = %s',(nome_delete, id_user))
    resultado = cursor.fetchone()
    idtamplate = resultado[0]
    cursor.execute('DELETE FROM favoritos WHERE id = %s AND user_id_user = %s',(idtamplate, id_user))
    connection.commit()
    connection.close()

