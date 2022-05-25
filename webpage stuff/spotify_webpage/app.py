from flask import Flask, render_template, request
import requests

import runmodel
import spotify as sp
app = Flask(__name__) #this has 2 underscores on each side


response = []
song_url = '';


@app.route('/',methods=['GET', 'POST'])
def base():
	print('here1!')
	search_query = request.form.get('search')
	print(search_query)
	if(search_query != '' and search_query != None):
		response = sp.search(search_query)
		print(response)
		return render_template('base.html.j2', results=response)
	return render_template('base.html.j2',genre='123')

def url_for():
	print('hiii')

@app.route('/song',methods=['GET', 'POST'])
def song():
	print('here2!')
	song_url = request.args.get('url')
	print(song_url)
	return render_template('base.html.j2', results=response, song_url=song_url)
