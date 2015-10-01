__author__ = 'adityaw@erasysconsulting.com'

from flask import Flask, redirect, url_for, session, request, render_template
from flask_oauthlib.client import OAuth
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
app.debug = True
# set the secret key.  keep this really secret:
app.secret_key = 'development'
oauth = OAuth(app)

ggid = oauth.remote_app(
    'ggid',
    consumer_key='your app id', #change this accordingly
    consumer_secret='your app secret', #change this accordingly
    request_token_params={'scope': 'all'},
    base_url='https://gg-id.net/api/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://gg-id.net/o/token/',
    authorize_url='https://gg-id.net/o/authorize/?app=x' #change this accordingly
)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/login")
def login():
    if 'ggid_token' in session:
        return redirect(url_for('profile'))
    else:
        return ggid.authorize(callback=url_for('authorized', _external=True))


@app.route("/popup-login")
def popup_login():
    if 'ggid_token' in session:
        return redirect(url_for('profile'))
    else:
        return ggid.authorize(state="popup", callback=url_for('authorized', _external=True))


@app.route("/logout")
def logout():
    #not production tested, use at your own risk
    session.clear()
    return redirect(url_for('index'))


@ggid.tokengetter
def get_ggid_token(token=None):
    return session.get('ggid_token')


@app.route('/consumer/exchange/')
def authorized():
    resp = ggid.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )

    # example what is returned from the GG-ID server
    # {u'access_token': u'ACCESS_TOKEN', u'token_type': u'Bearer', u'expires_in': 36000, u'refresh_token': u'REFRESH_TOKEN', u'scope': u'all'}
    session['ggid_token'] = (resp['access_token'], '')
    session['refresh_token'] = resp['refresh_token']

    me = ggid.get('users/me')
    session['user'] = me.data

    if request.args.get('state') == 'popup':
        return redirect(url_for('popup'))
    else:
        return redirect(url_for('profile'))

@app.route("/popup")
def popup():
    return render_template('popup.html')

@app.route("/me")
def profile():
    if 'ggid_token' in session:
        me = ggid.get('users/me')
        session['user'] = me.data

        return render_template('profile.html')
    else:
        return redirect(url_for('login'))

if __name__ == "__main__":
    # import os
    # os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    handler = RotatingFileHandler('/tmp/flask-ggid.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)
    app.run()