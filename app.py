# -*- coding: utf-8 -*-
"""
Created on Mon Aug  2 14:13:04 2021

@author: ramak
"""
from flask import Flask, render_template, request, redirect, url_for, session
#from flask_mysqldb import MySQL
#import MySQLdb.cursors
import sqlite3 as s
import re
import json
import requests
import pandas as pd
responsej = requests.get("https://s3-ap-southeast-1.amazonaws.com/he-public-data/courses26269ff.json").json()
response=pd.DataFrame(responsej)
app = Flask(__name__)
  
  
app.secret_key = 'key'
conn=s.connect('data.db')
c=conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS 'accounts'('id' INTEGER NOT NULL primary key AUTOINCREMENT,'username' TEXT NOT NULL,'password' TEXT NOT NULL,'email' TEXT NOT NULL);")
conn.commit()
conn.close()



'''  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'your password'
app.config['MYSQL_DB'] = 'geeklogin'
  
mysql = MySQL(app)
'''  
@app.route('/')
@app.route('/index', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        conn=s.connect('data.db')
        cursor =conn.cursor()
        cursor.execute('SELECT * FROM accounts WHERE username = "{}" AND password = "{}"'.format(str(username), str(password), ))
        account = cursor.fetchone()
        print(account)
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[1]
            msg = 'Logged in successfully !'
            return render_template('dash1.html', msg = responsej)
        else:
            msg = 'Incorrect username / password !'
        #conn.commit()
        conn.close()
    return render_template('login.html', msg = msg)
  
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))
  
@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        conn=s.connect('data.db')
        cursor =conn.cursor()
        cursor.execute('SELECT * FROM accounts WHERE username = "{}"'.format(username))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, "{}", "{}", "{}")'.format(username, password, email))
            #mysql.connection.commit()
            msg = 'You have successfully registered !'
        conn.commit()
        conn.close()
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html')
@app.route('/courses/<int:page_id>')
def page(page_id):
    # Replace with your custom code or render_template method
    d=responsej[page_id-1]
    #print(d)
    videolink=[]
    for i in d['videoLink']:
        videolink.append(i.replace('https://youtu.be/',''))
    return render_template('courses-details.html', msg = d,video=videolink)
@app.route('/pay/<int:page_id>')
def paypage(page_id):
    # Replace with your custom code or render_template method
    d=responsej[page_id-1]
    return render_template('pay.html', msg = d)

if __name__ == '__main__':
    app.run(debug=True)