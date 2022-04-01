from flask import Flask, render_template, request 
import requests
app = Flask(__name__) #this has 2 underscores on each side 
 
@app.route('/',methods=['GET', 'POST']) 
def index(): 

	return render_template('index.html.j2') 

# def req_spotify(data):
# 	response = requests.get("http://api.open-notify.org/astros.json")
# 	print(response)
# 	print('cool')

 
# def get_spotify_auth():
	
# 	print('ok')


@app.route('/callback',methods=['GET', 'POST']) 
def callback():
	if(request.form.get('search') != None):
		req_spotify(request.form.get('search'))

		print(request.form.get('search'))