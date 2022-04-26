import mysql.connector
import static.conexoes.autho_mysql as autho

host=autho.host
db=autho.database
user=autho.user
password=autho.password
port = autho.port

conn = mysql.connector.connect(host=host, user=user, password=password, db=db)
cursor = conn.cursor()

def share_report():
    pass
share_report()