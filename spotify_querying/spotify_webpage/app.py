from flask import Flask, render_template, request 
import requests
# import request
import spotify as sp
app = Flask(__name__) #this has 2 underscores on each side 
 

response = []
song_url = '';


@app.route('/',methods=['GET', 'POST']) 
def index():

	if(request.data):
		print(request.data)
	if(request.form.get('search') != None):
		search_query = request.form.get('search')
		response = sp.search(search_query)
		print(response)
		return render_template('index.html.j2',results=response, song_url=song_url) 
	return render_template('index.html.j2') 


@app.route('/song',methods=['GET', 'POST'])
def song():
	print('here!')
	song_url = request.args.get('url')
	print(song_url)

	# print('woah')
	return render_template('index.html.j2', results=response, song_url=song_url) 	