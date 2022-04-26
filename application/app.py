from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
from pathlib import Path
from configparser import ConfigParser

# importa modulos criados
import modulos.periodo as dashboardapp
from modulos.deleta import deleta_dashboard
from modulos.fun_SQL import cadastro, conexoes, cadastro_adm, mostra_equipe
from modulos.conector_facebookads import page_impressions, page_views_total

# configura conexão com DB
ini_config = str(Path('application\\config\\config.ini').resolve())
init_config = ini_config
config = ConfigParser()
config.read(init_config)

# inicia um servidor flask
app = Flask(__name__, template_folder="tamplates")

# inicia conexão com DB
try:
    app.secret_key = 'super secret key'
    app.config['MYSQL_HOST'] = config.get('DB','host')
    app.config['MYSQL_USER'] = config.get('DB', 'user')
    app.config['MYSQL_PASSWORD'] = config.get('DB', 'password')
    app.config['MYSQL_DB'] = config.get('DB','database')
    
    mysqldata = MySQL(app)
    print('Conexão realizada com sucesso')

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
    cursor.execute(f'SELECT NOME_DASHBOARD, THUMBNAIL, URL FROM tbd_salvos INNER JOIN tbd_tamplates ON tbd_tamplates.ID = tbd_salvos.ID WHERE ID_USUARIO = {id_user}')
    records = cursor.fetchall()
    if records:
        records=records
    else:
        h1 = 'Você ainda não criou nada!'
        p = 'Que tal gerar grandes insights com apenas alguns cliques?'
    
    # deleta uma conexao
    if request.method == 'POST':
        deleta_dashboard(id_user=id_user, nome_delete= request.form['delete'])
        
    return render_template('dash.html', p=p, h1=h1, saudacao=saudacao, avatar=avatar, records=records)

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

@app.route('/equipes', methods=['GET', 'POST'])
def equipes():
    avatar = session['username'][0]
    id_user = session['id']

    # mostra equipe
    cursor = mysqldata.connection.cursor(MySQLdb.cursors.DictCursor)
    
    empresa = mostra_equipe(id=id_user)

    cursor.execute(f'SELECT NOME, SOBRENOME, EMAIL FROM tbd_usuario WHERE EMPRESA = "{empresa}"')
    resultado = cursor.fetchall()
    
    # adiciona_membro_equipe
    if request.method == 'POST' and 'nome' in request.form and 'sobrenome' in request.form and 'email' in request.form:
        nome = request.form['nome']
        sobrenome = request.form['sobrenome']
        email = request.form['email']
        
        cadastro_adm(nome=nome, sobrenome=sobrenome, email=email)

    return render_template('equipes.html', avatar=avatar, membros=resultado)

@app.route('/salvar', methods=['GET', 'POST'])
def salvar():
    if request.method == 'POST' and 'nome_tamplate' in request.form:
        nome_dash = request.form['nome_dash']
        nome_tamplate = request.form['nome_tamplate']
        user = session['id']

        cursor = mysqldata.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(f'SELECT ID FROM tbd_tamplates WHERE NOME_TAMPLATE = "{nome_tamplate}"')
        resultador = cursor.fetchone()

        # idconn = resultador['id_conexao']
        idtamplate = resultador['ID']

        cursor.execute('INSERT INTO tbd_salvos (NOME_DASHBOARD, ID_USUARIO, ID_TAMPLATES, ID_CONEXAO) VALUES (%s,%s,%s,%s)', (nome_dash,user, idtamplate, "1"))
        mysqldata.connection.commit()

        return redirect(url_for(f'{nome_tamplate}'))
   
    return redirect(url_for('tamplates_vendas'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():

    return render_template('user_profile.html')
 
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

    return render_template('register.html')


# # tamplates 
@app.route('/facebookinsights', methods =['GET', 'POST'])
def facebookinsights():
    radiobutton = 'last_year'

    if request.method == 'POST' and 'radiobutton' in request.form:
        periodo = request.form['radiobutton']
        
        if periodo == 'Ontem':
            radiobutton = 'yesterday'

        elif periodo == 'Mês passado':
            radiobutton = 'last_month'


    return render_template('facebookads.html', impressoes=page_impressions(), visitas=page_views_total())


if __name__ == "__main__":
    app.run(debug=True, port=8080)
