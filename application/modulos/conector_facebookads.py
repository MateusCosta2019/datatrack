import pandas as pd
import facebook
from datetime import datetime
import json 

params = dict()
params['page_token'] = 'EAAUTdastuisBAH6QUqFivmN8XH8YiIyjfqLX9zZAN72bQqT9iICiSZAZA3bjZBdOoOJZAY4qNYJzUtjwfIZAXQES5iSY0wWC2Y9DbSZA0oqZCXL5KE6FMYwe16eBcZC9zd5ZAu55ch0QEEu2fpHfpCFsZBPbYOHddZAwODQV0EVTS4yo3EXyvt0uqVumDkeuuIKtKNGrkXEGRmstRgF0i1U25DYZC'        # not an actual access token
params['page_id'] = '101161708771914' 
graph = facebook.GraphAPI(access_token=params['page_token'], version="3.1")

filtro_data = 'last_year'

def page_impressions():
    page_impressions = graph.get_connections(id=params['page_id'], connection_name='insights', 
                                            metric='page_impressions',
                                            date_preset=filtro_data,
                                            show_description_from_api_doc=False)

    dados = page_impressions['data'][0]['values']
    df = pd.DataFrame(dados)
    df['end_time'] = pd.to_datetime(df['end_time'], errors='coerce')
    df['end_time'] = df['end_time'].dt.strftime('%m-%d-%y')
    df['end_time'] = pd.to_datetime(df['end_time'])
    dfs = df.resample(rule='M', on='end_time').agg({'value':'sum'}).reset_index()
    
    
    dfs['end_time'] = dfs['end_time'].dt.strftime('%d-%b-%y')
    dfs.rename({"end_time": "x", "value": "y"}, axis=1, inplace=True)
    dad = dfs.to_dict(orient='records')
    
    return dad

def page_views_total():
    page_views_total = graph.get_connections(id=params['page_id'], connection_name='insights', 
                                            metric='page_views_total',
                                            date_preset=filtro_data,
                                            show_description_from_api_doc=False)

    dados = page_views_total['data'][0]['values']
    df = pd.DataFrame(dados)
    df['end_time'] = pd.to_datetime(df['end_time'], errors='coerce')
    df['end_time'] = df['end_time'].dt.strftime('%m-%d-%y')
    df['end_time'] = pd.to_datetime(df['end_time'])
    dfs = df.resample(rule='M', on='end_time').agg({'value':'sum'}).reset_index()
    
    
    dfs['end_time'] = dfs['end_time'].dt.strftime('%m-%b-%y')
    dfs.rename({"end_time": "x", "value": "y"}, axis=1, inplace=True)
    dados_finais = dfs.to_dict(orient='records')
    
    return dados_finais

def page_fans_gender_age():
    page_fans_gender_age = graph.get_connections(id=params['page_id'], connection_name='insights', 
                                            metric='page_views_total',
                                            date_preset='last_year',
                                            # period='day',
                                            show_description_from_api_doc=False)

    # dados = page_fans_gender_age['data'][0]['values']
    # df = pd.DataFrame(dados)
    # df['end_time'] = pd.to_datetime(df['end_time'], errors='coerce')
    # df['end_time'] = df['end_time'].dt.strftime('%m-%d-%y')
    # df['end_time'] = pd.to_datetime(df['end_time'])
    # dfs = df.resample(rule='M', on='end_time').agg({'value':'sum'}).reset_index()
    
    
    # dfs['end_time'] = dfs['end_time'].dt.strftime('%m-%b-%y')
    # dfs.rename({"end_time": "x", "value": "y"}, axis=1, inplace=True)
    # dados_finais = dfs.to_dict(orient='records')
    
    return page_fans_gender_age

print(page_fans_gender_age())