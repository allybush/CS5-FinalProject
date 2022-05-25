from flask import Flask, render_template, request, redirect
import requests
# import request
import runmodel
import spotify as sp
app = Flask(__name__) #this has 2 underscores on each side


response = []
song_url = ''


@app.route('/', methods=['GET', 'POST'])
def index():
	if(request.data):
		print(request.data)
	if(request.form.get('search') != None):
		search_query = request.form.get('search')
		response = sp.search(search_query)
		return render_template('base.html.j2',results=response)
	return render_template('base.html.j2')


@app.route('/song', methods=['POST'])
def song():
	return render_template('base.html.j2')
	# print('woah')
	#return render_template('base.html.j2', results=response, song_url=song_url, decision = decision)
@app.route('/results', methods = ['POST'])
def results():
	response=request.form.get("url")
	#runs model on it
	#returns decision/image
	if(response != None):
		return response
	else:
		return "hi"
