from flask import Flask, render_template, request, session, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flask_mysqldb import MySQL
from spotipy.oauth2 import SpotifyClientCredentials
import json
import math,spotipy




app = Flask(__name__)

#configure mysql
app.config['MYSQL_HOST'] = 'mysql.2122.lakeside-cs.org'
app.config['MYSQL_USER'] = 'student2122'
app.config['MYSQL_PASSWORD'] = 'm545CS42122'
app.config['MYSQL_DB'] = '2122project'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['SECRET_KEY']='lol'
mysql=MySQL(app)

#https://medium.com/@maxtingle/getting-started-with-spotifys-api-spotipy-197c3dc6353b  this guy helped me set up the credentials
#https://spotipy.readthedocs.io/en/latest/#module-spotipy.client api documentation


#setting up spotipy
cid='97657ba98a784f6e9427ad8d2ca6678c'
secret='efd404699e244125b3a211d52532d3c2'
client_credentials_manager=SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp=spotipy.Spotify(client_credentials_manager=client_credentials_manager)

#setting up genres and genres with spaces (for display)
genres=['Billboard_Top_100', 'Rap', 'Indie_Pop', 'Classical', 'Country', 'Reggae', 'R&B', 'Classic_Rock', 'Christmas']
spacegenres=['Billboard Top 100', 'Rap', 'Indie Pop', 'Classical', 'Country', 'Reggae', 'R&B', 'Classic Rock', 'Christmas']

#Setting up information
playlist=[]
songs= []
songsimages= []
songsname = []
#this helped me with jsons:
#https://medium.com/@kemepley/how-to-navigate-jsons-in-python-e826807aa3be

#more setup of the playlists
playlist.append(sp.playlist('https://open.spotify.com/playlist/6yOYKjOY6gXew3X9FlFgOq?si=5d07a4e2a3894cb0'))
playlist.append(sp.playlist('https://open.spotify.com/playlist/4riovLwMCrY3q0Cd4e0Sqp?si=d18818f843ec4537'))
playlist.append(sp.playlist('https://open.spotify.com/playlist/37i9dQZF1DWWEcRhUVtL8n?si=dd89c780936f47a2'))
playlist.append(sp.playlist('https://open.spotify.com/playlist/1h0CEZCm6IbFTbxThn6Xcs?si=dd7710490e1e4b44'))
playlist.append(sp.playlist('https://open.spotify.com/playlist/0J74JRyDCMotTzAEKMfwYN?si=1cddf118e681441e'))
playlist.append(sp.playlist('https://open.spotify.com/playlist/37i9dQZF1EQpjs4F0vUZ1x?si=b85322157dfd4dfc'))
playlist.append(sp.playlist('https://open.spotify.com/playlist/37i9dQZF1EQoqCH7BwIYb7?si=0c5e9d54186a4e86'))
playlist.append(sp.playlist('https://open.spotify.com/playlist/6TeyryiZ2UEf3CbLXyztFA?si=57827d3e471147c8'))
playlist.append(sp.playlist('https://open.spotify.com/playlist/37i9dQZF1DX6R7QUWePReA?si=0bc42fd988d14a25'))

#setting up the songs in each playlist
for i in range(len(playlist)):
    songs1=[]
    songsimages1=[]
    songsname1=[]
    for x in range(20):
        songs1.append(playlist[i]['tracks']['items'][x+1]['track']['external_urls']['spotify'])
        songsimages1.append(playlist[i]['tracks']['items'][x+1]['track']['album']['images'][1]['url'])
        addsong=playlist[i]['tracks']['items'][x+1]['track']['name']
        if "(feat" in addsong:
            findindex = int(addsong.find('(feat'))
            addsong=addsong[0:findindex]
        songsname1.append(addsong)

    songs.append(songs1)
    songsimages.append(songsimages1)
    songsname.append(songsname1)
#end of information



@app.route('/', methods=['GET', 'POST'])
def index():
    #logout system
    if request.method=="POST":
        session.pop('allybush_username', None)
    if session.get('allybush_username')!= None:
        username=session.get('allybush_username') #transfers username to index so it can display it on screen.
        username=username.upper()
        return render_template('index.html', username=username, session=True)
    else:
        return render_template('index.html', session=False)


@app.route('/foryou',methods=['GET', 'POST'])
def foryou():
    if session.get('allybush_username')!=None:
        #sends the genres liked to template so it can display them on the page along with the corresponding songs.
        genresliked=queryGenresLiked()
        return render_template('foryou.html', songs=songs, playlist=playlist, songsimages=songsimages, songsname=songsname,
        genres=genres, genresliked=genresliked, spacegenres=spacegenres)
    else:
        #need two separate returns for session and no session because genresliked depends on who is logged in.
        return render_template('foryou.html', songs=songs, playlist=playlist, songsimages=songsimages, songsname=songsname,
        genres=genres, spacegenres=spacegenres)

@app.route('/friends', methods=['GET', 'POST'])
def friends():
    error=False
    #connects to mysql
    cursor=mysql.connection.cursor()
    #gets session name
    sessionname=session.get('allybush_username')
    #gets friend list
    query='SELECT friends FROM allybush_login WHERE username LIKE BINARY %s'
    #gets friend list for user from mysql so it can display on screen
    queryvars=(sessionname,)
    cursor.execute(query,queryvars)
    mysql.connection.commit()
    friends=cursor.fetchall()
    friends=friends[0]['friends']
    friends=friends.split()

    #uses friend list to get song
    friendsfavsong=[]
    friendsfavartist=[]
    friendsfavname=[]

    #if the user has friends then run this, necessary to ensure that it doens't throw indexing error.
    if friends:
        query='SELECT favsong, favsongname, favsongartist FROM allybush_login WHERE username IN %s'
        queryvars=(friends,)
        cursor.execute(query,queryvars)
        mysql.connection.commit()
        results=cursor.fetchall()
        for x in range(len(friends)):
            #adds the favorite song url, artists, and song name of your friends to arrays
            #arrays are passed to template to display
            friendsfavsong.append(results[x]['favsong'])
            friendsfavartist.append(results[x]['favsongartist'])
            friendsfavname.append(results[x]['favsongname'])

        #if the user wants to edit their favorite song
    if request.method=="POST":
        cursor=mysql.connection.cursor()
        sessionname=session.get('allybush_username')

        favsongname=str(request.form.get("favsongname"))
        favsongartist=str(request.form.get("favsongartist"))
        if favsongname and favsongartist:
            favsongquery=favsongname + " " + favsongartist #this part was challenging because it doesn't follow the standard spotify query format: spotipy uses its dropdown
            #queries their favorite song based on what they entered
            favsong=sp.search(q=favsongquery, type="track")
            if len(favsong['tracks']['items']) >0:
                favsong= favsong['tracks']['items'][0]['external_urls']['spotify']
                favsong=sp.track(favsong)
                #sets up information to update.
                if len(favsong) > 0:
                    favsongtitle=favsong['name']
                    favsongartist2=favsong['album']['artists'][0]['name']
                    favsong=favsong['album']['images'][0]['url']
                else:
                    #returns errors later after the page updates current friendsfavsong in order to not repeat large chunks of code
                    error=True
            else:
                error=True
        else:
            error=True

        #makes sure the length of favsong>0
        if not error:
            #updates the database with the information they entered
            query='UPDATE allybush_login SET favsong=%s, favsongname=%s, favsongartist=%s WHERE username LIKE BINARY %s'
            queryvars=(favsong,favsongtitle, favsongartist2, sessionname,)
            cursor.execute(query,queryvars)
            mysql.connection.commit()

            #gets own song link
            query='SELECT favsong, favsongname, favsongartist FROM allybush_login WHERE username LIKE BINARY %s'
            queryvars=(sessionname,)
            cursor.execute(query,queryvars)
            mysql.connection.commit()
            results=cursor.fetchall()
            #stuff to display
            myfavsong=results[0]['favsong']
            myfavartist=results[0]['favsongartist']
            myfavname=results[0]['favsongname']

            return render_template('friends.html', favsong=favsong, favsongquery=favsongquery, friendsfavsong=friendsfavsong, myfavsong=myfavsong, friends=friends,
            sessionname=sessionname, friendsfavname=friendsfavname, friendsfavartist=friendsfavartist, myfavname=myfavname, myfavartist=myfavartist)
        else:
            #gets song information to return along with the error
            query='SELECT favsong, favsongname, favsongartist FROM allybush_login WHERE username LIKE BINARY %s'
            queryvars=(sessionname,)
            cursor.execute(query,queryvars)
            mysql.connection.commit()
            results=cursor.fetchall()
            myfavsong=results[0]['favsong']
            myfavartist=results[0]['favsongartist']
            myfavname=results[0]['favsongname']

            return render_template('friends.html',  error=True, friendsfavsong=friendsfavsong, myfavsong=myfavsong, friends=friends,
            sessionname=sessionname, friendsfavname=friendsfavname, friendsfavartist=friendsfavartist, myfavname=myfavname, myfavartist=myfavartist)
    else:
        #gets own song link
        query='SELECT favsong, favsongname, favsongartist FROM allybush_login WHERE username LIKE BINARY %s'
        queryvars=(sessionname,)
        cursor.execute(query,queryvars)
        mysql.connection.commit()
        results=cursor.fetchall()
        #same stuff as before essentially
        myfavsong=results[0]['favsong']
        myfavartist=results[0]['favsongartist']
        myfavname=results[0]['favsongname']
        return render_template('friends.html', friendsfavsong=friendsfavsong, sessionname=sessionname, friends=friends, myfavsong=myfavsong,
        results=results, friendsfavname=friendsfavname, friendsfavartist=friendsfavartist, myfavname=myfavname, myfavartist=myfavartist)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=="GET":
        #this runs if the user wants to login
        return render_template('login.html', validfield=True)
    else:
        #this runs if the server is trying authenticate the user's user and pass.
        enterusername=request.form.get("enterusername")
        enterpassword=request.form.get("enterpassword")
        if enterusername and enterpassword:
            query='SELECT password FROM allybush_login WHERE username=%s'
            queryvars=(enterusername,)
            cursor=mysql.connection.cursor()
            cursor.execute(query,queryvars)
            mysql.connection.commit()
            dbpassword=cursor.fetchall()
            if(dbpassword!=None):
                dbpassword=dbpassword[0]['password'] #gets database pass
                if (check_password_hash(dbpassword,enterpassword)==True): #checks database pass with the one entered using checkhash()
                    session['allybush_username'] = enterusername
                    return redirect(url_for('index')) #this is the success
                else:
                    #all of these else statements are errors, but specific errors that login.html displays
                    return render_template('login.html', dbpassword=dbpassword, enterpassword=enterpassword, validfield=False)
            else:
                return render_template('login.html', dbpassword=dbpassword, enterpassword=enterpassword, validfield=False)
        else:

            return render_template('login.html', dbpassword=dbpassword, enterpassword=enterpassword, validfield=False)

@app.route('/newaccount', methods=['POST', 'GET'])
def newaccount():
    #this runs if the server is trying to see if the username is duped or invalid, then it inputs into database
    if request.method=="POST":
        newusername=request.form.get("newusername")
        query = 'SELECT username FROM allybush_login WHERE username LIKE BINARY %s'
        queryvars= (newusername,)
        cursor=mysql.connection.cursor()
        cursor.execute(query,queryvars)
        mysql.connection.commit()
        findusername= cursor.fetchall()
        if(len(findusername) == 0):
            if ( " " in newusername or len(newusername)< 3):##this section inspired by the login code given by Ms. O'Neal
                return render_template('newaccount.html', invaliduser=True)
            else:
                newpassword=request.form.get("newpassword")
                hashedpassword=generate_password_hash(newpassword) #makes sure the password is secure by using someone else's hash function
                query = 'INSERT INTO allybush_login (username,password) VALUES (%s, %s)'
                queryvars= (newusername, hashedpassword,)
                cursor.execute(query,queryvars)
                mysql.connection.commit()
                return redirect(url_for('login')) #if successful, it redirects to the login page
                #this runs if the user is trying to create a new account
        else:
            return render_template('newaccount.html', alreadyexists=True)
    else:
        return render_template('newaccount.html')
@app.route('/editgenre', methods=['POST', 'GET'])
def editgenre():
    cursor=mysql.connection.cursor()
    if request.method=="POST": #if the user wants to edit their favorite genres
        genreslikedstring=""
        for x in range(0,len(genres)):
            genresliked=request.form.get(genres[x]) #each form has an id of genres[x], so it refers to that id to request.
            if(genresliked!= None):
                genreslikedstring=genreslikedstring+ " " + genres[x] #genres are in one column of the database, space-separated.

        query = 'UPDATE allybush_login SET genresliked=%s WHERE username=%s'
        sessionname=session.get('allybush_username')
        queryvars= (genreslikedstring,sessionname,)
        cursor.execute(query,queryvars)
        mysql.connection.commit()
        genresliked=queryGenresLiked()
        #above, i created a function because i found myself querying the genres mulitple times with the exact same block of code
        return render_template('editgenre.html', genres=genres, genresliked=genresliked, spacegenres=spacegenres, update=True)
    else:
        genresliked=queryGenresLiked()
        #again, genres
        return render_template('editgenre.html', genres=genres, genresliked=genresliked, spacegenres=spacegenres)

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    #simply just redirecting, this page is kind of a placeholder
    return redirect(url_for('index'))

@app.route('/editfriends', methods=['POST', 'GET'])
def editfriends():
    cursor=mysql.connection.cursor()
    sessionname=session.get('allybush_username')
    if request.method=="POST":
        #gets the friends information so all of the following if statements can use these variables in their operators.
        friends=queryFriends()
        friendsarray=sortFriends(friends)
        #again, setup for the if statements
        addfriend=request.form.get("addfriend")
        #makes sure the person entered a valid field
        if addfriend != None:
            #makes sure the person isn't trying to add themselves
            if addfriend==sessionname:
                return render_template('editfriends.html', youruser=True, friendsarray=friendsarray)
            #makes sure the person hasn't already added them
            elif not addfriend in friends:
                query = 'SELECT username FROM allybush_login WHERE username=%s'
                queryvars= (addfriend,)
                cursor.execute(query,queryvars)
                mysql.connection.commit()
                iffriend=cursor.fetchall()
                #iffriend is the results from asking the database if username is even a valid user
                if not iffriend:
                    return render_template('editfriends.html', nonexistent=True, friendsarray=friendsarray)
                #the successful case: adds the friend to database if it passes all of these tests
                else:
                    friends=friends + " " + addfriend
                    query = 'UPDATE allybush_login SET friends=%s WHERE username=%s'
                    queryvars= (friends,sessionname,)
                    cursor.execute(query,queryvars)
                    mysql.connection.commit()
                    #has to query friends again to update the page because you just added someone to the list
                    friends=queryFriends()
                    friendsarray=sortFriends(friends)
                    return render_template('editfriends.html', success=True, friendsarray=friendsarray, iffriend=iffriend)
            else:

                return render_template('editfriends.html', alreadyfriend=True, friendsarray=friendsarray)

        else:
            return render_template('editfriends.html', blankuser=True, friendsarray=friendsarray)
    else:
        #makes sure the page has updated friend information
        friends=queryFriends()
        friendsarray=sortFriends(friends)
        return render_template('editfriends.html', friendsarray=friendsarray)

#redirect for removefriend ajax
@app.route('/removefriend', methods=['POST'])
def removefriend():
    #takes the button from js's post  (jquery $.ajax)
    buttonname = request.form['button']
    cursor=mysql.connection.cursor()
    #gets the friends list
    query='SELECT friends FROM allybush_login WHERE username=%s'
    sessionname=session.get('allybush_username')
    queryvars=(sessionname,)
    cursor.execute(query,queryvars)
    mysql.connection.commit()
    friends=cursor.fetchall()
    friends=friends[0]['friends']

    #removes the person from the friends list by slicing
    if buttonname in friends:
        friendsindex=friends.index(buttonname)
        friends=friends[0:friendsindex] + friends[friendsindex+len(buttonname):len(friends)]
    #updates the database with updated friends information
    query='UPDATE allybush_login SET friends=%s WHERE username=%s'
    queryvars=(friends,sessionname,)
    cursor.execute(query,queryvars)
    mysql.connection.commit()
    #returns something so js knows this chunk is done
    return buttonname
    #success function runs rn.


##used because I called the same block of code twice and was too lazy to rewrite it.
def queryGenresLiked():
    cursor=mysql.connection.cursor()
    query = 'SELECT genresliked FROM allybush_login WHERE username=%s'
    sessionname= session.get('allybush_username')
    queryvars= (sessionname,)
    cursor.execute(query,queryvars)
    mysql.connection.commit()
    genresliked=cursor.fetchall()
    genresliked=genresliked[0]['genresliked']
    return genresliked
def queryFriends():
    cursor=mysql.connection.cursor()
    query = 'SELECT friends FROM allybush_login WHERE username=%s'
    sessionname=session.get('allybush_username')
    queryvars= (sessionname,)
    cursor.execute(query,queryvars)
    mysql.connection.commit()
    results=cursor.fetchall()
    friends=results[0]['friends']
    return friends

def sortFriends(friends):
    if(" " in friends):
        friendsarray=friends.split()
    elif len(friends)==1:
        friendsarray=[friends]
    else:
        friendsarray=()
    return friendsarray
