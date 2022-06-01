//takes random number/path and gives it to python side then takes genre and displays
function getRandom()
{
  //stops audio from player
  document.getElementById("newplayer").pause();
  //makes the page look like it refreshed/clean
  clearBelow();
  loadingGif();
  var path = document.getElementById("link").href;
  path = "path=" + path;
  var xhttp = new XMLHttpRequest();
  xhttp.open('POST', '/song', true);
  xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
//executes when call is successful
  xhttp.onreadystatechange = function() {
    if(xhttp.readyState == 4 && xhttp.status == 200) {
        var response = JSON.parse(xhttp.responseText);
        //parses JSON and gets genre
        response = response['result'];
        //changes text in the genre modal to the genre result.
        document.getElementById("firstrow").innerHTML = "Your random audio was classified as \"" + response + "\"";
        document.getElementById("secondrow").innerHTML = "";
        var imagesrc = "static/genre_img/" + response + ".jpeg";
        document.getElementById("genre_img").src = imagesrc;
        //displays the link to the results
        document.getElementById("genrebutton").style.display = "block";
        document.getElementById("spectrogram").style.display = "block";
        //takes away loading gif
        removeGif();
    }
  }
  //submits post request
  xhttp.send(path);

}

//shorthand function for adding the loading gif
function loadingGif()
{
  var loadingdiv = document.getElementById("decision");
  var loadinggif = document.createElement("img");
  loadinggif.id = "loadinggif";
  loadinggif.src = "static/loading.gif";
  loadinggif.style.height = "150px";
  //centers on page
  loadinggif.style.margin = "auto";
  loadingdiv.appendChild(loadinggif);
}
//fucntion for removing loading gif
function removeGif()
{
  document.getElementById("loadinggif").remove();
}
//clears the genre button and spectrogram so page looks like it's refreshed
function clearBelow()
{
  document.getElementById('genrebutton').style.display = "none";
  document.getElementById('spectrogram').style.display = "none";
}
//gets song data from selected song when the user clicks a song
function getSongData(url, artists, songname) {
  //indicates process is occurring
    loadingGif();
    clearBelow();
    // puts parameters into proper urlencoded form
    var param = "url=" + url;
    var xhttp = new XMLHttpRequest();
    console.log(param);
    //opens post request to /song
    xhttp.open('POST', '/song', true);
    //important so we can access the data at ['url'] in python side
    xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    //runs when post request is successful
    xhttp.onreadystatechange = function() {
      if(xhttp.readyState == 4 && xhttp.status == 200) {
        //parses response into JSON
          var response = JSON.parse(xhttp.responseText);
          //parses JSON into string we want
          response = response['result'];
          //changes genre modal inner text to the result
          document.getElementById("firstrow").innerHTML = songname + " by " + artists;
          console.log(artists);
          document.getElementById("secondrow").innerHTML = "was classified as \"" + response + "\"";
          //path for image to display in modal
          var imagesrc = "static/genre_img/" + response + ".jpeg";
          document.getElementById("genre_img").src = imagesrc;
          document.getElementById("spectrogram").style.display = "block";
          //stops the loading gif and shows the genre button for results
          removeGif();
          document.getElementById("genrebutton").style.display = "block";
      }
    }
    //sends post request
    xhttp.send(param);

  }
//submits user input and searches spotify for songs
function submitChoices()
{
  //checks if stuff is still on page, if so it removes
  if(document.getElementById('myUL')!= null)
  {
    document.getElementById('myUL').remove();
  }
  if(document.getElementById('error')!= null)
  {
    document.getElementById('error').remove();
  }
  //gets text entered in the box
  var input = document.getElementById('input').value;
  console.log(input);
  //creates list for the resulting songs
  var newlist = document.createElement("ul");
  newlist.id = "myUL";
  var listdiv = document.getElementById('listdiv');
  //shows error if no text inputted
  if(input=="")
  {
    var nonefound = document.createElement("li");
    nonefound.innerHTML = "You must enter text.";
    newlist.appendChild(nonefound);
    listdiv.appendChild(newlist);

  }
  //sends input to python side in urlencoded post request
  else {
    input = "input=" + input;
    var xhttp = new XMLHttpRequest();
    xhttp.open('POST', '.', true);
    xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    var submit = document.getElementById("submitbutton");
    //shows visual of loading
    submit.innerHTML = "Loading...";

    xhttp.onreadystatechange = function() { //Call a function when the state changes.
      if(xhttp.readyState == 4 && xhttp.status == 200) {
        //parses json and indexes response
            var response = JSON.parse(xhttp.responseText);
            response = response['response'];
            console.log(response);
            //checks if there's an error or if no songs are found
            if (response == "NOTFOUND" || response.length == 0) // thx to this person for the logic https://levelup.gitconnected.com/different-ways-to-check-if-an-object-is-empty-in-javascript-e1252d1c0b34
            {
              var error = document.createElement("p");
              //changes text to red and displays error message
              error.id = 'error';
              error.style.color = "red";
              error.innerHTML = "No songs found — check spelling.";
              listdiv.appendChild(error);

            }
            //checks if random error—this would only occur if someone did something very weird trying to hack
            if (response == "NO")
            {
              var error = document.createElement("p");
              error.id = 'error';
              error.style.color = "red";
              error.innerHTML = "Error — what did you even do to get this message???";

            }

            else {
              //use list for artist name to capture multiple artists. have to use list because I
              //tested a single variable and it would just print the last artist for every song because of the variable changing per song.
              artistname = [];
              //loops through every song in the returned JSON
              for(let i=0; i<response.length;i++)
              {
                //checks if there's a 30 second preview we can use. if not, it just jumps to next index.
                if(response[i]['preview_url'])
                {
                  //adds list element with onclick of getsongData and href of nothing.
                  var temp = document.createElement("li");
                  var link  =  document.createElement("a");
                  temp.class = "close";
                  temp.setAttribute('data-dismiss', 'modal');
                  link.href = '#';
                  if (response[i].hasOwnProperty('artists') && response[i]['artists'].length > 0 )
                  {
                    //adds artist to a temporary string that is later added to the artsit array
                    tempartist = response[i]['artists'][0]['name'];
                    for (let x = 1; x < response[i]['artists'].length; x++)
                    {
                      //appends artist to existing list with some formatting.
                      tempartist += ", " + response[i]['artists'][x]['name'];
                    }
                    artistname.push(tempartist);
                  }
                  else
                  {
                    artistname.push("Unidentified Artist");
                  }
                  //uses arrays for everything so the data doesn't get mixed between songs
                  link.onclick = function () {getSongData(response[i]['preview_url'], artistname[i], response[i]['name'])};
                  console.log(artistname);
                  //changes text of the dropdown to the name and artist
                  link.innerHTML = response[i]['name'] + " — " + artistname[i];
                  temp.appendChild(link);
                  newlist.appendChild(temp);
                }
                else
                {
                  //increases list index so the JSON index and artistname index stay aligned.
                  artistname.push("");
                }
              }
              listdiv.appendChild(newlist);
              submit.innerHTML = "Submit!";
          }
      }
    }
    //sends post request
    xhttp.send(input);
  }

}
//creates random path for wav file in the random modal.
  function random(){
    //removes player if modal is clicked on.
    if(document.getElementById("newplayer"))
    {
      document.getElementById("newplayer").remove();
    }
    //creates random path using Math.random()
     var soundFile = "static/songs/"+Math.round(Math.random() * (50 - 1) + 1)+".wav";
     //creates new link to the wav file (not because we want the link but because we want to access it in a different function)
     document.getElementById("player1").innerHTML= "<a href=\""+soundFile+"\" id=\"link\"  />";
     //creates button called Use that calls the function to submit the wav file.
     document.getElementById("link").innerHTML += "<button class='btn btn-secondary' id=\"usebutton\" onclick='getRandom();' data-dismiss = 'modal'>Use</button>";
     var usebutton =  document.getElementById("usebutton");
     usebutton.style.marginLeft = "210px";
     usebutton.style.marginBottom = "10px";
     usebutton.style.width = "60px";
     //code to create the audio player onscreen so users can test the audio before they use.
     var newplayer = document.createElement("audio");
     // thanks to this person for the help https://stackoverflow.com/questions/37735208/create-audio-element-dynamically-in-javascript
     newplayer.id =  "newplayer";
     newplayer.controls = 'controls';
     newplayer.src =  soundFile;
     document.getElementById('player').appendChild(newplayer);
     // https://developer.mozilla.org/en-US/docs/Web/API/Event/preventDefault thanks for this one mozilla!!
     // prevent default for clicking on the usebutton link, otherwise it would leave the page and take us to the wav file in static.
     document.querySelector("#usebutton").addEventListener("click", function(event) {
         event.preventDefault();
       }, false);

}
