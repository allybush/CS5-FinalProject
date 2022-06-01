from flask import Flask, render_template, request, jsonify
import requests

import runmodel
import spotify as sp
import spotipy
app = Flask(__name__) #this has 2 underscores on each side



@app.route('/',methods=['GET', 'POST'])
def base():
	#checks if there's the request is for spotify search or not
	if(request.method == 'POST'):
		#checks if input is passed
		if(request.form.get('input') != None):
			#gets input from url
			search_query = request.form.get('input')
			print(search_query)
			response = sp.search(search_query)
			return jsonify(response=response)
		else:
			return "NO"
	#if not post request, just returns normal page
	return render_template('base.html.j2')

@app.route('/song', methods=['POST'])
def song():
	#address = url for the song in question
	address = request.form.get('url')
	#checks if the reason for post request is for song info or path info (path info is for random, url info is for spotify)
	if(address!= None):
		#runs model on url
		result = runmodel.run(address)
		#returns genre
		return jsonify(result=result)
	path = request.form.get('path')
	if(path!= None):
		#runs model on path given by random wav file (path is url)
		result = runmodel.run(path)
		return jsonify(result=result)
	else:
		return "Could not find URL for song"
