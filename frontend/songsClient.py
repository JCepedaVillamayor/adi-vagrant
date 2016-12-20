#!/usr/bin/python
# -*- coding: utf-8; mode: python -*-

from flask import Flask, request, redirect, url_for, g, session, flash, render_template
import json
from flask_oauthlib.client import OAuth

app = Flask(__name__)
app.secret_key = 'secret'
oauth = OAuth(app)


CLIENT_ID = '0FFiZ6bKh9zrXW5puXMQhyXYN3VSz75gWy4HubAl'
CLIENT_SECRET = 'pnmIfZiDmBDcJJY6M1kYsIO3jHBpakrqeA4DCeCeUJ5fVHMHvn'

remote = oauth.remote_app(
    'remote',
    consumer_key=CLIENT_ID,
    consumer_secret=CLIENT_SECRET,
    request_token_params={'scope': 'email'},
    base_url='http://172.19.145.246:8000/',
    request_token_url='http://172.19.145.246:8000/oaut/authorized',
    access_token_url='http://172.19.145.246:8000/oauth/token',
    authorize_url='http://172.19.145.246:8000/oauth/authorize'
)


# Obtener token para esta sesion
@remote.tokengetter
def get_remote_token(token=None):
    if 'remote_oauth' in session:
        return session.get('remote_oauth')


# Limpiar sesion anterior e incluir la nueva sesion
@app.before_request
def before_request():
    g.user = None
    if 'remote_oauth' in session:
        g.user = session['remote_oauth']


# Pagina principal
@app.route('/')
def index():
    songs = None
    if g.user is not None:
        resp = remote.request('songs')
        if resp.status == 200:
            data = resp.data
            songs = data['songs']
        else:
            flash('You do not have authorization.')
    return render_template('index.html', songs=songs)


# Get auth token (request)
@app.route('/login')
def login():
    next_url = request.args.get('next') or request.referrer or None
    resp= remote.authorize(
        callback=url_for('oauthorized', _external=True)
    )
    return resp


# Eliminar sesion
@app.route('/logout')
def logout():
    session.pop('remote_oauth', None)
    return redirect(url_for('index'))


# Callback
@app.route('/oauthorized')
def oauthorized():
    resp = remote.authorized_response()
    if resp is None:
        flash('You do not have enough permissions.')
    else:
        session['remote_oauth'] = resp
    return redirect(url_for('index'))



# Operaciones
@app.route('/postSong', methods=['POST'])
def addSong():
    if g.user is None:
        return redirect(url_for('login', next=request.url))
    songTitle = request.form['songTitle']
    songAlbum = request.form['songAlbum']
    if not songTitle or not songAlbum:
        return redirect(url_for('index'))
    resp = remote.request('songs', data=json.dumps({'title':songTitle,'album':songAlbum}), method='POST', content_type="application/json")
    if resp.status == 401:
        flash('You do not have enough permissions', 'error')
    else:
        print resp.data
        flash('Song added (ID: #%s)' % resp.data['created'], 'success')
    return redirect(url_for('index'))

@app.route('/delSong', methods=['POST'])
def delSong():
    if g.user is None:
        return redirect(url_for('login', next=request.url))
    songID = request.form['songID']
    if not songID:
        return redirect(url_for('index'))
    resp = remote.request('songs/'+songID, method='DELETE', content_type="application/json")
    if resp.status == 401:
        flash('You do not have enough permissions.', 'error')
    elif resp.status == 404:
        flash('Song not found.', 'error')
    else:
        flash('Song deleted (ID: #%s)' % resp.data['deleted'], 'success')
    return redirect(url_for('index'))



if __name__ == '__main__':
    import os
    os.environ['DEBUG'] = 'true'
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'
    app.run(host='0.0.0.0', port=9000, debug=True)
