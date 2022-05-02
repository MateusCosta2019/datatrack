from flask import Flask, render_template, url_for, redirect
from authlib.integrations.flask_client import OAuth
import os

from requests import session

app = Flask(__name__, template_folder="tamplates")
app.secret_key = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O/<!\xd5\xa2\xa0\x9fR"\xa1\xa8'

oauth = OAuth(app)

@app.route('/')
def index():
	return render_template('index.html')

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
			'scope': 'openid email profile'
		}
	)
	
	# Redirect to google_auth function
	redirect_uri = url_for('google_auth', _external=True)
	return oauth.google.authorize_redirect(redirect_uri)

@app.route('/google/auth/')
def google_auth():
	token = oauth.google.authorize_access_token()
	print(" Google User ", token)
    
	return redirect('/')

@app.route('/facebook/')
def facebook():

	# Facebook Oauth Config
	FACEBOOK_CLIENT_ID = os.environ.get('FACEBOOK_CLIENT_ID')
	FACEBOOK_CLIENT_SECRET = os.environ.get('FACEBOOK_CLIENT_SECRET')
	oauth.register(
		name='facebook',
		client_id=FACEBOOK_CLIENT_ID,
		client_secret=FACEBOOK_CLIENT_SECRET,
		access_token_url='https://graph.facebook.com/oauth/access_token',
		access_token_params=None,
		authorize_url='https://www.facebook.com/dialog/oauth',
		authorize_params=None,
		api_base_url='https://graph.facebook.com/',
		client_kwargs={'scope': 'email'},
	)
	redirect_uri = url_for('facebook_auth', _external=True)
	return oauth.facebook.authorize_redirect(redirect_uri)

@app.route('/facebook/auth/')
def facebook_auth():
	token = oauth.facebook.authorize_access_token()
	resp = oauth.facebook.get(
		'https://graph.facebook.com/me?fields=id,name,email,picture{url}')
	profile = resp.json()
	print("Facebook User ", profile)
	return redirect('/')

if __name__ == "__main__":
	app.run(debug=True)
