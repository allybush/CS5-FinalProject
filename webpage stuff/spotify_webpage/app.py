from flask import Flask, render_template, request, jsonify
import requests

import runmodel
import spotify as sp
app = Flask(__name__) #this has 2 underscores on each side


response = []
song_url = '';


@app.route('/',methods=['GET', 'POST'])
def base():
	if(request.method == 'POST'):
		if(request.form.get('input') != None):
			search_query = request.form.get('input')
			print(search_query)
			response = sp.search(search_query)
			return jsonify(response=response)
		else:
			return "NO"
	song_name = 'Search and Destroy'
	artist_name = 'the Stooges'
	genre = 'rock'
	path = '/genre_img/'+ genre +'.jpeg'
	return render_template('base.html.j2',song_name=song_name,artist_name=artist_name,genre=genre,path=path)

# def url_for():
# 	print('hiii')

@app.route('/song', methods=['POST'])
def song():
	print(request.form.get('url'))
	address = request.form.get('url')
	if(address!= None):
		result = runmodel.run(address)
		print(result)
		return jsonify(result=result)
	else:
		return "Could not find URL for song"
