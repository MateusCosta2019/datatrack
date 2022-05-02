from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
from pathlib import Path
from configparser import ConfigParser
import logging 
from datetime import datetime
import string
import random
from authlib.integrations.flask_client import OAuth
import os

# importa modulos criados
import modulos.periodo as dashboardapp
from modulos.deleta import deleta_dashboard
from modulos.fun_SQL import cadastro, conexoes, cadastro_adm, mostra_equipe
from modulos.conector_facebook import post_alcance, media_gender, total_engajamento, metricas, total_actions, media_age, page_views_total, page_fans, page_fans_last_month, clicks_on_page, fans_groth

# configura conexão com DB
ini_config = str(Path('application\\config\\config.ini').resolve())
init_config = ini_config
config = ConfigParser()
config.read(init_config)

# inicia um servidor flask
app = Flask(__name__, template_folder="tamplates")
oauth = OAuth(app)


# inicia conexão com DB
try:
    app.secret_key = 'super secret key'
    app.config['MYSQL_HOST'] = config.get('DB','host')
    app.config['MYSQL_USER'] = config.get('DB', 'user')
    app.config['MYSQL_PASSWORD'] = config.get('DB', 'password')
    app.config['MYSQL_DB'] = config.get('DB','database')
    
    mysqldata = MySQL(app)

except Exception as erro:
    print("ERRO: MYSQL-erro-code", erro)
    exit()

@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'senha' in request.form:
        email = request.form['email']
        senha = request.form['senha']

        cursor = mysqldata.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT ID, NOME, SOBRENOME, EMAIL, SENHA FROM tbd_usuario WHERE EMAIL = %s AND SENHA = MD5(%s)', (email, senha))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['email'] = account['EMAIL']
            session['password'] = account['SENHA']
            session['username'] = account['NOME']
            session['id'] = account['ID']
            msg = 'Logged in successfully !'
            
            return redirect(url_for('dashboard'))
        else:
            msg = 'Senha ou usuário incorreto!'

    return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('email', None)
    return redirect(url_for('login'))

@app.route('/dashboard', methods =['GET', 'POST'])
def dashboard():   
    h1 = ''
    p = ''
    cursor = mysqldata.connection.cursor(MySQLdb.cursors.DictCursor)
    
    saudacao = dashboardapp.saudacao()
    id_user = session['id']
    avatar = session['username'][0]

    # Pega dashboards salvos
    cursor.execute(f'SELECT NOME_DASHBOARD, THUMBNAIL, tbd_salvos.URL, DATA_CRIACAO FROM tbd_salvos INNER JOIN tbd_tamplates ON tbd_tamplates.ID = tbd_salvos.ID WHERE ID_USUARIO = {id_user}')
    records = cursor.fetchall()
    if records:
        records=records
    else:
        h1 = 'Você ainda não criou nada!'
        p = 'Que tal gerar grandes insights com apenas alguns cliques?'
    
    # deleta uma conexao
    if request.method == 'POST':
        deleta_dashboard(id_user=id_user, nome_delete= request.form['delete'])
        
    return render_template('inicio.html', p=p, h1=h1, saudacao=saudacao, avatar=avatar, records=records)

@app.route('/dashboard_share_with_you', methods =['GET', 'POST'])
def dashboard_compartilhados():   
    h1 = ''
    p = ''
    cursor = mysqldata.connection.cursor(MySQLdb.cursors.DictCursor)
    
    saudacao = dashboardapp.saudacao()
    id_user = session['id']
    avatar = session['username'][0]

    # Pega dashboards salvos
    cursor.execute(f'SELECT ID_TAMPLATE FROM tbd_compartilhados WHERE ID_USUARIO_COMP = {id_user};')
    ID_TAMPLATE_ = cursor.fetchone()
    ID_TAMPLATE = ID_TAMPLATE_
    print(ID_TAMPLATE)

    cursor.execute(f'SELECT NOME_DASHBOARD, THUMBNAIL, tbd_salvos.URL FROM tbd_salvos INNER JOIN tbd_tamplates ON tbd_tamplates.ID = tbd_salvos.ID WHERE tbd_tamplates.ID = 1')
    records = cursor.fetchall()
    if records:
        records=records
    else:
        h1 = 'Que pena, ninguém compratilhou nenhum dashboard com você'
            
    return render_template('dash_compatilhados.html', p=p, h1=h1, saudacao=saudacao, avatar=avatar, records=records)


@app.route('/conexao', methods =['GET', 'POST'])
def conexao():
    avatar = session['username'][0]

    # exibe conexoes do usuario
    erroconexoes=''
    suberro=''

    id_user = session['id']
    dados = conexoes(id=id_user)
    n_conexoes = []
    id_conexao = []

    if dados:
        for row in dados:
            n_conexoes.append(row['nome_conexao'])
            id_conexao.append(row['id_conexao'])
            
    else:
        erroconexoes = 'Você não possui nenhuma fonte de dados'
        suberro = 'Faça uma conexão'
    
    # deleta uma conexao
    # if request.method == 'POST' and 'excluir' in request.form:
    #     query = request.form['excluir']
    #     cursor.execute('DELETE FROM conexoes WHERE nome_conexao = %s AND table1_id_user = %s',(query, id_user))
    #     mysqldata.connection.commit()

    return render_template('conexoes.html' , erroconexoes=erroconexoes, suberro=suberro, conexoes=n_conexoes, avatar=avatar)   

@app.route('/tamplates', methods=['GET', 'POST'])
def tamplates():
    avatar = session['username'][0]
    # ====================== exibe conexoes do usuario ==================================
    id_user = session['id']
    cursor = mysqldata.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(f'SELECT NOME_CONEXAO FROM tbd_conexoes WHERE ID_USUARIO = {id_user}')
    dados = cursor.fetchall()
    nomecon = []
    if dados:
        for row in dados:
            nomecon.append(row['nome_conexao'])
            
    else:
        info = 'Você não possui nenhuma fonte de dados'
    # ====================== exibe conexoes do usuario ==================================


    # ====================== carrega base de tamplates ==================================
    msg=''
    cursor = mysqldata.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT ID, NOME_TAMPLATE, URL, THUMBNAIL FROM tbd_tamplates')
    records = cursor.fetchall()
    if records == None:
        msg = 'Erro ao carregar nossos tamplates, tente novamente dentro de alguns minutos ou entre em contato com nosso suporte.'
    # ====================== carrega base de tamplates ==================================

    return render_template('tamplates_vendas.html', msg=msg, records=records, avatar=avatar)

@app.route('/salvar', methods=['GET', 'POST'])
def salvar():
    if request.method == 'POST' and 'nome_tamplate' in request.form:
        nome_tamplate = request.form['nome_tamplate']
        user = session['id']

        cursor = mysqldata.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(f'SELECT URL FROM tbd_tamplates WHERE NOME_TAMPLATE = "{nome_tamplate}"')
        resultador = cursor.fetchone()
        url_base = resultador['URL']

        escolhas_possiveis = string.ascii_letters + string.digits
        resultado = ''
        for i in range(50):
            resultado += random.choice(escolhas_possiveis)

        novo_url = url_base+'/'+resultado
        chave_unica = novo_url[39:]

        cursor.execute('INSERT INTO tbd_salvos (NOME_DASHBOARD, ID_USUARIO,ID_TAMPLATES, URL, ID_CONEXAO, DATA_CRIACAO) VALUES (%s,%s,%s, %s, %s, NOW())', (nome_tamplate ,user, 1, novo_url, "1"))
        mysqldata.connection.commit()

        return redirect(url_for(f'{nome_tamplate+"/"+chave_unica}'))
   
    return redirect(url_for('tamplates'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():

    return render_template('perfil.html')
 
@app.errorhandler(404) 
def not_found(e): 
  
  return render_template("404.html") 

@app.route('/registro', methods =['GET', 'POST'])
def registro():
    
    if request.method == 'POST' and 'nome' in request.form and 'sobrenome' in request.form and 'email' in request.form and 'senha' in request.form:
        nome = request.form['nome']
        sobrenome = request.form['sobrenome']
        email = request.form['email']
        senha = request.form['senha']
        
        cadastro(nome=nome, sobrenome=sobrenome, email=email, senha=senha)
        return redirect(url_for('login'))

    return render_template('cadastro.html')

# # tamplates 
@app.route('/testedesgraca', methods =['GET', 'POST'])
def facebookinsights():

    #################### DECLARAÇÃO DE VARIAVEIS #################### 
    msg = ''
    periodo = ''
    periodo_imprimi = ''
    url_end = request.base_url
    print(url_end)
    alcance=post_alcance(filtro=periodo)
    visitas=page_views_total(filtro=periodo)
    seguidores = page_fans()
    seguidores_ = page_fans_last_month()
    acoes = clicks_on_page()
    crescimento = fans_groth(filtro=periodo)
    metrica_ =metricas()
    media_idade =media_age(filtro=periodo)
    media_genero =media_gender(filtro=periodo)
    total_acoes =total_actions(filtro=periodo)
    engajamento_total =total_engajamento()
    
    #################### VALIDAÇÃO DO BOTÃO DE FILTRO ####################
    if request.method == 'POST' and 'exampleRadios' in request.form:
        periodo = request.form['exampleRadios']
        print(periodo)

    else:
        print("filtro inexistente")

    #################### FUNÇÃO DE COMPARTILHAR DASHBOARD ####################
    
    #################### VALIDA PERIODO E RETORNA NO DASHBOARD ####################
    if periodo == 'today':
        periodo_imprimi = 'Hoje'
    
     
    return render_template('facebookinsights.html',
    msg = msg,
    alcance=alcance, 
    visitas=visitas,
    page_fans = seguidores,
    page_fans_last_28d = seguidores_,
    clicks_on_page = acoes,
    fans_groth = crescimento,
    metricas=metrica_,
    media_age=media_idade,
    media_gender=media_genero,
    total_actions=total_acoes,
    total_engajamento=engajamento_total,
    periodo_imprimi=periodo_imprimi)


@app.route('/facebook_insights/<name>', methods =['GET', 'POST'])
def apenas(name=None):

    msg = ''
    periodo = ''
    periodo_imprimi = ''
    url_end = request.base_url
    print(url_end)
    alcance=post_alcance(filtro=periodo)
    visitas=page_views_total(filtro=periodo)
    seguidores = page_fans()
    seguidores_ = page_fans_last_month()
    acoes = clicks_on_page()
    crescimento = fans_groth(filtro=periodo)
    metrica_ =metricas()
    media_idade =media_age(filtro=periodo)
    media_genero =media_gender(filtro=periodo)
    total_acoes =total_actions(filtro=periodo)
    engajamento_total =total_engajamento()

    return render_template(
    'facebookinsights.html',
    name=name,
    msg = msg,
    alcance=alcance, 
    visitas=visitas,
    page_fans = seguidores,
    page_fans_last_28d = seguidores_,
    clicks_on_page = acoes,
    fans_groth = crescimento,
    metricas=metrica_,
    media_age=media_idade,
    media_gender=media_genero,
    total_actions=total_acoes,
    total_engajamento=engajamento_total,
    periodo_imprimi=periodo_imprimi)


@app.route('/google/')
def google():

	GOOGLE_CLIENT_ID = '1024109355929-73jshc403dcggmp7tast0k1tscd5mk33.apps.googleusercontent.com'
	GOOGLE_CLIENT_SECRET = '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'
	CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
	oauth.register(
		name='google',
		client_id=GOOGLE_CLIENT_ID,
		client_secret=GOOGLE_CLIENT_SECRET,
		server_metadata_url=CONF_URL,
		client_kwargs={
			'scope': 'https://www.googleapis.com/auth/analytics.readonly'
		}
	)
	
	# Redirect to google_auth function
	redirect_uri = url_for('google_auth', _external=True)
	return oauth.google.authorize_redirect(redirect_uri)

@app.route('/google/auth/')
def google_auth():
	token = oauth.google.authorize_access_token()
	print(" Google User ", token)
    
	return redirect(url_for('conexao'))

if __name__ == "__main__":
    app.run(debug=True, port=8080)
