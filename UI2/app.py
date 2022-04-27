from flask_mysqldb import MySQL
from flask import Flask, render_template, request

app = Flask(__name__)
@app.route('/')

def index():
    return render_template('index.html')
