from configparser import ConfigParser
from pathlib import Path
import mysql.connector

ini_config = str(Path('application\\config\\config.ini').resolve())

def conecta_db():

    """
    Realiza a conexão com o banco de dados MYSQL
    
    Params:
        Args:

        Return:
            Conector para banco de dados MYSQL
    """

    init_config = ini_config
    config = ConfigParser()
    config.read(init_config)

    try:
        connection = mysql.connector.connect(host=config['DB']['host'], port=config['DB']['port'], user=config['DB']['user'],
        password=config['DB']['password'], db=config['DB']['database'])

        print("Você está conectado")
        print("___________________")
    
    except Exception as erro:
        print("ERRO: MYSQL-erro-code", erro)
        exit()

    return connection
    