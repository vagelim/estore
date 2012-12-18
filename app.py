#!/bin/env python
from flask import Flask, session, redirect, url_for, escape, request
from flask import render_template, url_for
import os
from login import valid_login, logmein, create_login, valid_username, saltPassword
import msg as msg

app = Flask(__name__)

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html')
    username = request.cookies.get('username')
    if 'username' in session:
        return 'Cookie for %s' % escape(session['username'])
    return 'You are not logged in'

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        if valid_username(username) == False:
            #Should render a page saying username is taken
            return False
        password = saltPassword(request.form['password'])
        create_login(username,password)#MUST send HASHED PW to create_login -> everything else takes unhashed and does hashing
        return render_template('index.html')

    if request.method == 'GET':
       return render_template('signup.html')


@app.route('/message', methods=['GET', 'POST'])
def message():
    from time import gmtime, strftime

    if request.method == 'POST':
        return render_template('message.html', sender = session['username'], receiver = request.form['username'], message= request.form['message'], timestamp = str(strftime("%Y-%m-%d %H:%M:%S", gmtime())) )
    if request.method == 'GET':
        return render_template('message.html', username = session['username'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if valid_login(request.form['username'],
            request.form['password']):
            return logmein(request.form['username'])
        else:
            error = 'Invalid username/password'
        # the code below this is executed if the request method
        # was GET or the credentials were invalid
            return render_template('signup.html')
    if request.method == 'GET':
        return render_template('login.html')
    
@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
    app.run(debug=True)
