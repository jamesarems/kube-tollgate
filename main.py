#!/usr/bin/env python3

from flask import Flask, render_template, redirect, g, url_for
from flask_oidc import OpenIDConnect
import subprocess

app = Flask(__name__)
app.config.update({
    'SECRET_KEY': 'SomethingNotEntirelySecret',
    'TESTING': True,
    'DEBUG': True,
    'OIDC_CLIENT_SECRETS': '/kube-tollgate/config/client_secrets.json',
    'OIDC_ID_TOKEN_COOKIE_SECURE': False,
    'OIDC_REQUIRE_VERIFIED_EMAIL': False,
    'OIDC_USER_INFO_ENABLED': True,
    'OIDC_SCOPES': ['openid', 'email', 'profile'],
    'OIDC_INTROSPECTION_AUTH_METHOD': 'client_secret_post'
    #'OVERWRITE_REDIRECT_URI': 'https://dev.logcop.io/*'
})

oidc = OpenIDConnect(app)


@app.route('/')
def home():
    if oidc.user_loggedin:
        info = oidc.user_getinfo(['preferred_username', 'email', 'sub', 'given_name', 'iss'])
        from oauth2client.client import OAuth2Credentials
        try:
        	id_token = OAuth2Credentials.from_json(oidc.credentials_store[info.get('sub')]).id_token_jwt
        except KeyError:
        	id_token = 'Null'
        username = info.get('preferred_username')
        iss = info.get('iss')
        refresh_token = oidc.get_refresh_token()
        return render_template('index.html', name=username, access=id_token, refresh=refresh_token, iss=iss)
    else:
        return redirect('/login')

@app.route('/login')
@oidc.require_login
def login():
    info = oidc.user_getinfo(['preferred_username', 'email', 'sub'])
    username = info.get('preferred_username')
    return redirect('/')

@app.route('/logout')
def logout():
    oidc.logout()
    return redirect('/')
    #response = redirect(url_for('/'))
    #response.set_cookie(OIDC.id_token_cookie_name, expires=0)
    #return response


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=2222)
