from getdatagoogle import get_data_from_google_sheets
import pandas as pd
from conecta_db import conecta_db

connection = conecta_db()
cursor = connection.cursor()

def dashboard_google_sheets(id_user):
    cursor.execute(f'SELECT id_planilha, variancia FROM conexoes INNER JOIN favoritos ON conexoes_id_conexao = id_conexao WHERE user_id_user = {id_user}')
    data = cursor.fetchall()
    range = ''
    planilha = ''
    for n in data:
        range = (n[1])
        planilha = (n[0])

    print(range, planilha)
    data = get_data_from_google_sheets(SAMPLE_SPREADSHEET_ID_input=planilha, SAMPLE_RANGE_NAME=range)
    return data
   
def tamplate_sales(tipo_conexao, id_user):

    dados = dashboard_google_sheets(id_user=id_user)
    cliente = []
    data_compra = []
    data_entrega = []
    sinal_pedido = []
    sub_total = []
    custo_frete = []
    avaliacao = []

    list_of_rows = dados
    for row in list_of_rows:
        cliente.append(row[1])
        data_compra.append(row[2])
        data_entrega.append(row[3])
        sinal_pedido.append(row[4])
        sub_total.append(row[5])
        custo_frete.append(row[6])
        avaliacao.append(row[7])

    data_dic = {
        "x": data_compra,
        "y": sub_total
    }
    df = pd.DataFrame(data_dic)
    df['y'] = df['y'].astype(float, errors = 'raise')
    agrr = df.groupby(df['x'], as_index=False)["y"].sum()
    
    dados_vol = agrr.to_dict(orient='list')
    return dados_vol

