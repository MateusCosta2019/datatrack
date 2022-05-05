import re
import pandas as pd
import facebook
from datetime import datetime
import json 

params = dict()
params['page_token'] = 'EAAUTdastuisBAA6hiHhLyNRl9MshJPajnSvLTYMgdulwuoS1CeAWk44aowe7E5g3wf5ssXjer9zxZBqG3WYxwHDOnP7NIogN6XkAWZADutt3hjnmrhyq3DiIF4qM04exJyf9V3zp8v6P7AEshnBnGh8wwr9toAJd5I9zfPjkiIXFK61woyYKQbtTvJ0DQTQkdUHRCoDZBJ2vJsqnTmB'        # not an actual access token
params['page_id'] = '623594861616145' 
graph = facebook.GraphAPI(access_token=params['page_token'], version="3.1")

filtro_data = 'last_month'

def post_alcance(filtro):
    Impressoes = graph.get_connections(id=params['page_id'], 
                                    connection_name='insights', 
                                    metric='page_impressions',
                                    date_preset=filtro)

    dados_Impressoes = Impressoes['data'][0]['values']
    df_impressoes = pd.DataFrame(dados_Impressoes, columns=['value', 'end_time'])

    df_impressoes['end_time'] = pd.to_datetime(df_impressoes['end_time'], errors='coerce')
    df_impressoes['end_time'] = df_impressoes['end_time'].dt.strftime('%m-%d-%y')
    df_impressoes['end_time'] = pd.to_datetime(df_impressoes['end_time'])
    agraga = df_impressoes.resample(rule='D', on='end_time').agg({'value':'sum'}).reset_index()


    agraga['end_time'] = agraga['end_time'].dt.strftime('%d-%m-%y')
    agraga.rename({"end_time": "x", "value": "y"}, axis=1, inplace=True)
    dados_finais = agraga.to_dict(orient='records')
    
    return dados_finais

def page_views_total(filtro):
    page_views_total = graph.get_connections(id=params['page_id'], connection_name='insights', 
                                            metric='page_views_total',
                                            date_preset=filtro,
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

def page_fans():
    page_impressions = graph.get_connections(id=params['page_id'], connection_name='insights', 
                                            metric='page_fans',
                                            date_preset='today',
                                            show_description_from_api_doc=False)

    dados = page_impressions['data'][0]
    page_fans = dados['values'][0]['value']
    return page_fans

def page_fans_last_month():
    page_fans_last = graph.get_connections(id=params['page_id'], connection_name='insights', 
                                            metric='page_fans',
                                            date_preset=filtro_data,
                                            show_description_from_api_doc=False)

    dados = page_fans_last['data'][0]['values']
    df = pd.DataFrame(dados)
    df['end_time'] = pd.to_datetime(df['end_time'], errors='coerce')
    df['end_time'] = df['end_time'].dt.strftime('%m-%d-%y')
    df['end_time'] = pd.to_datetime(df['end_time'])
    valor = df['value'].iloc[-7]
    return valor

def clicks_on_page():
    page_total_actions = graph.get_connections(id=params['page_id'], connection_name='insights', 
                                            metric='page_total_actions',
                                            date_preset='last_30d',
                                            show_description_from_api_doc=False)

    dados = page_total_actions['data'][0]['values']
    df_page_total_actions = pd.DataFrame(dados)
    df_page_total_actions['end_time'] = pd.to_datetime(df_page_total_actions['end_time'], errors='coerce')
    df_page_total_actions['end_time'] = df_page_total_actions['end_time'].dt.strftime('%m-%d-%y')
    df_page_total_actions['end_time'] = pd.to_datetime(df_page_total_actions['end_time'])
    # agrega_df_page_total_actions = df_page_total_actions.resample(rule='M', on='end_time').agg({'value':'sum'}).reset_index()


    df_page_total_actions['end_time'] = df_page_total_actions['end_time'].dt.strftime('%d-%b-%y')
    df_page_total_actions.rename({"end_time": "x", "value": "y"}, axis=1, inplace=True)
    dados_finais = df_page_total_actions.to_dict(orient='records')
    return dados_finais

def fans_groth(filtro):
    page_fans = graph.get_connections(id=params['page_id'], connection_name='insights', 
                                            metric='page_fans',
                                            date_preset=filtro,
                                            show_description_from_api_doc=False)

    dados = page_fans['data'][0]['values']
    df_page_fans = pd.DataFrame(dados)
    df_page_fans['end_time'] = pd.to_datetime(df_page_fans['end_time'], errors='coerce')
    df_page_fans['end_time'] = df_page_fans['end_time'].dt.strftime('%m-%d-%y')
    df_page_fans['end_time'] = pd.to_datetime(df_page_fans['end_time'])
    # agrega_df_page_total_actions = df_page_total_actions.resample(rule='M', on='end_time').agg({'value':'sum'}).reset_index()


    df_page_fans['end_time'] = df_page_fans['end_time'].dt.strftime('%d-%m-%y')
    df_page_fans.rename({"end_time": "x", "value": "y"}, axis=1, inplace=True)
    dados_finais = df_page_fans.to_dict(orient='records')   
    return dados_finais

def media_age(filtro):
    page_fans_gender_age = graph.get_connections(id=params['page_id'], connection_name='insights', 
                                            metric='page_fans_gender_age',
                                            date_preset=filtro,
                                            show_description_from_api_doc=False)

    dados = page_fans_gender_age['data'][0]['values']
    df_page_fans_gender_age = pd.DataFrame(dados[0], columns=['value', 'end_time'])
    df_page_fans_gender_age.drop(["end_time"], axis=1, inplace=True)
    df_page_fans_gender_age['idade'] = df_page_fans_gender_age.index
    df_page_fans_gender_age.rename({"value": "Seguidores"}, axis=1, inplace=True)

    df_page_fans_gender_age[['Sexo', 'Idade']] = df_page_fans_gender_age['idade'].str.split('.', 1, expand=True)
    del df_page_fans_gender_age['idade']
    df_page_fans_gender_age.reset_index(drop=True, inplace=True)

    df2 = df_page_fans_gender_age.groupby(df_page_fans_gender_age.Sexo)
    feminino = df2.get_group('F')
    maculino = df2.get_group('M') 
    del feminino['Sexo']
    del maculino['Sexo']
    feminino.rename({"Seguidores": "y", "Idade": "x"}, axis=1, inplace=True)
    maculino.rename({"Seguidores": "y", "Idade": "x"}, axis=1, inplace=True)
    dados_finaism = maculino.to_dict(orient='records')
    dados_finaisf = feminino.to_dict(orient='records')

    return([dados_finaisf, dados_finaism])

def media_gender(filtro):
    page_fans_gender_age = graph.get_connections(id=params['page_id'], connection_name='insights', 
                                            metric='page_fans_gender_age',
                                            date_preset=filtro,
                                            show_description_from_api_doc=False)

    dados = page_fans_gender_age['data'][0]['values']
    df_page_fans_gender_age = pd.DataFrame(dados[0], columns=['value', 'end_time'])
    df_page_fans_gender_age.drop(["end_time"], axis=1, inplace=True)
    df_page_fans_gender_age['idade'] = df_page_fans_gender_age.index
    df_page_fans_gender_age.rename({"value": "Seguidores"}, axis=1, inplace=True)
    df_page_fans_gender_age[['Sexo', 'Idade']] = df_page_fans_gender_age['idade'].str.split('.', 1, expand=True)
    df_medias = df_page_fans_gender_age.groupby(['Sexo'], as_index=False)['Seguidores'].sum()
    base = sum(df_medias['Seguidores'])
    df_medias['Média'] = df_medias['Seguidores']/base*100
    df_medias['Média'] = round(df_medias['Média'], 2)
    del df_medias['Seguidores']
    df_medias.rename({"Sexo": "x", "Média": "y"}, axis=1, inplace=True)
    del df_medias['x']

    dadosfinais = df_medias['y'].to_list()

    return dadosfinais

def metricas():
    page_fans = graph.get_connections(id=params['page_id'], connection_name='insights', 
                                        metric='page_fans',
                                        date_preset='today',
                                        show_description_from_api_doc=False)

    dados = page_fans['data'][0]
    page_fans = dados['values'][0]['value']

    # _____________________________________________________________________________________________
    page_fan_adds_unique = graph.get_connections(id=params['page_id'], connection_name='insights', 
                                            metric='page_fan_adds_unique',
                                            date_preset='last_28d',
                                            show_description_from_api_doc=False)

    dados = page_fan_adds_unique['data'][0]
    page_fan_adds_unique = dados['values'][0]['value']

    # _____________________________________________________________________________________________
    page_impressions = graph.get_connections(id=params['page_id'], connection_name='insights', 
                                            metric='page_impressions',
                                            date_preset='last_28d',
                                            show_description_from_api_doc=False)

    dados = page_impressions['data'][0]
    page_impressions = dados['values'][0]['value']

    # _____________________________________________________________________________________________
    page_post_engagements = graph.get_connections(id=params['page_id'], connection_name='insights', 
                                            metric='page_post_engagements',
                                            date_preset='last_28d',
                                            show_description_from_api_doc=False)

    dados = page_post_engagements['data'][0]
    page_post_engagements = dados['values'][0]['value']

    # _____________________________________________________________________________________________
    df_dados = pd.DataFrame({
        'page_fans': [page_fans],
        'page_fan_adds_unique': [page_fan_adds_unique],
        'page_impressions': [page_impressions],
        'page_post_engagements': [page_post_engagements],
    })

    dados_finais = df_dados.to_dict(orient='records')


    return dados_finais

def total_actions(filtro):
    page_total_actions = graph.get_connections(id=params['page_id'], connection_name='insights', 
                                            metric='page_total_actions',
                                            date_preset=filtro,
                                            show_description_from_api_doc=False)
    dados = page_total_actions['data'][0]['values']
    df = pd.DataFrame(dados)
    del df['end_time']
    dados_finais = sum(df['value'])
    return dados_finais

def total_engajamento():
    page_post_engagements = graph.get_connections(id=params['page_id'], connection_name='insights', 
                                            metric='page_post_engagements',
                                            date_preset='last_year',
                                            show_description_from_api_doc=False)
    dados = page_post_engagements['data'][0]['values']
    df = pd.DataFrame(dados)
    del df['end_time']
    dados_finais = sum(df['value'])
    return dados_finais

def total_engajamento_post():
    post_engaged_users = graph.get_connections(id=params['page_id'], connection_name='insights', 
                                            metric='post_engaged_users',
                                            date_preset='last_year',
                                            show_description_from_api_doc=False)
    dados = post_engaged_users['data'][0]['values']
    df = pd.DataFrame(dados)
    del df['end_time']
    dados_finais = sum(df['value'])
    return dados_finais