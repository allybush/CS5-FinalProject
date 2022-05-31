function getRandom()
{
  document.getElementById("newplayer").pause();
  loadingGif();
  var path = document.getElementById("link").href;
  path = "path=" + path;
  var xhttp = new XMLHttpRequest();
  xhttp.open('POST', '/song', true);
  xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

  xhttp.onreadystatechange = function() { //Call a function when the state changes.
    if(xhttp.readyState == 4 && xhttp.status == 200) {
        var response = JSON.parse(xhttp.responseText);
        response = response['result'];
        document.getElementById("firstrow").innerHTML = "Your random audio was classified as \"" + response + "\"";
        document.getElementById("secondrow").innerHTML = "";
        var imagesrc = "/static/genre_img/" + response + ".jpeg";
        document.getElementById("genre_img").src = imagesrc;
        document.getElementById("genrebutton").style.display = "block";
        document.getElementById("spectrogram").style.display = "block";
        removeGif();
    }
  }
  xhttp.send(path);

}


function loadingGif()
{
  var loadingdiv = document.getElementById("decision");
  var loadinggif = document.createElement("img");
  loadinggif.id = "loadinggif";
  loadinggif.src = "static/loading.gif";
  loadinggif.style.height = "150px";
  loadinggif.style.margin = "auto";
  loadingdiv.appendChild(loadinggif);
}

function removeGif()
{
  document.getElementById("loadinggif").remove();
}

function getSongData(url, artists, songname) {
    loadingGif();
    console.log(url);
    console.log('here!!');
    document.getElementById('genrebutton').style.display = "none";

    var name = "url";
    var param = name + "=" + url;
    var xhttp = new XMLHttpRequest();
    console.log(param);
    xhttp.open('POST', '/song', true);
    xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

    xhttp.onreadystatechange = function() { //Call a function when the state changes.
      if(xhttp.readyState == 4 && xhttp.status == 200) {
          var response = JSON.parse(xhttp.responseText);
          response = response['result'];
          document.getElementById("firstrow").innerHTML = songname + " by " + artists;
          document.getElementById("secondrow").innerHTML = "was classified as \"" + response + "\"";
          var imagesrc = "/static/genre_img/" + response + ".jpeg";
          document.getElementById("genre_img").src = imagesrc;
          document.getElementById("spectrogram").style.display = "block";
          removeGif();
          document.getElementById("genrebutton").style.display = "block";
      }
    }
    xhttp.send(param);

  }

function submitChoices()
{

  if(document.getElementById('myUL')!= null)
  {
    document.getElementById('myUL').remove();
  }
  if(document.getElementById('error')!= null)
  {
    document.getElementById('error').remove();
  }
  var input = document.getElementById('input').value;
  console.log(input);
  var newlist = document.createElement("ul");
  newlist.id = "myUL";
  var listdiv = document.getElementById('listdiv');

  if(input=="")
  {
    var nonefound = document.createElement("li");
    nonefound.innerHTML = "You must enter text.";
    newlist.appendChild(nonefound);
    listdiv.appendChild(newlist);

  }
  else {
    input = "input=" + input;
    var xhttp = new XMLHttpRequest();
    xhttp.open('POST', '/', true);
    xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    var submit = document.getElementById("submitbutton");
    submit.innerHTML = "Loading...";

    xhttp.onreadystatechange = function() { //Call a function when the state changes.
      if(xhttp.readyState == 4 && xhttp.status == 200) {
            var response = JSON.parse(xhttp.responseText);
            response = response['response'];
            console.log(response);
            if (response == "NOTFOUND" || response.length == 0) // thx to this person for the logic https://levelup.gitconnected.com/different-ways-to-check-if-an-object-is-empty-in-javascript-e1252d1c0b34
            {
              var error = document.createElement("p");
              error.id = 'error';
              error.style.color = "red";
              error.innerHTML = "No songs found — check spelling.";
              listdiv.appendChild(error);

            }
            if (response == "NO")
            {
              var error = document.createElement("p");
              error.id = 'error';
              error.style.color = "red";
              error.innerHTML = "Error — what did you even do to get this message???";

            }
            else {
              for(let i=0; i<response.length;i++)
              {
                if(response[i]['preview_url'])
                {
                  var temp = document.createElement("li");
                  var link  =  document.createElement("a");
                  temp.class = "close";
                  temp.setAttribute('data-dismiss', 'modal');
                  link.href = '#';
                  if (response[i].hasOwnProperty('artists') && response[i]['artists'].length >0 )
                  {
                    var artistname = response[i]['artists'][0]['name'];
                    for (let x = 1; x < response[i]['artists'].length; x++)
                    {
                      artistname += ", " + response[i]['artists'][x]['name'];
                    }
                  }
                  else
                  {
                    var artistname = "Unidentified Artist";
                  }
                  link.onclick = function () {getSongData(response[i]['preview_url'], artistname, response[i]['name'])} ;
                  link.innerHTML = response[i]['name'] + " — " + artistname;
                  temp.appendChild(link);
                  newlist.appendChild(temp);
                }
              }
              listdiv.appendChild(newlist);
              submit.innerHTML = "Submit!";
          }
      }
    }
    xhttp.send(input);
  }

}

  function url_for(){
    console.log('test')
  }

  function button() { //this doesn't work for some reason
  var x = document.getElementById("rbutton");
  if (x.innerText == "Record Your Own Audio") {
    x.innerText = "Stop";
  } else {
    x.innerText = "Record Your Own Audio";
  }
  }

  function random(){
     var soundFile = "static/songs/"+Math.round(Math.random() * (50 - 1) + 1)+".wav";
     document.getElementById("player1").innerHTML= "<a href=\""+soundFile+"\" id=\"link\"  />";
     document.getElementById("link").innerHTML += "<button class='btn btn-secondary' id=\"usebutton\" onclick='getRandom();' data-dismiss = 'modal'>Use</button>";
     var usebutton =  document.getElementById("usebutton");
     usebutton.style.marginLeft = "210px";
     usebutton.style.marginBottom = "10px";
     usebutton.style.width = "60px";
     var newplayer = document.createElement("audio");
     // thanks to this person for the help https://stackoverflow.com/questions/37735208/create-audio-element-dynamically-in-javascript
     newplayer.id =  "newplayer";
     newplayer.controls = 'controls';
     newplayer.src =  soundFile;
     document.getElementById('player').appendChild(newplayer);
     // https://developer.mozilla.org/en-US/docs/Web/API/Event/preventDefault thanks for this one mozilla!!
     document.querySelector("#usebutton").addEventListener("click", function(event) {
         event.preventDefault();
       }, false);

}
      jQuery(document).ready(function () {
          var $ = jQuery;
          var myRecorder = {
              objects: {
                  context: null,
                  stream: null,
                  recorder: null
              },
              init: function () {
                  if (null === myRecorder.objects.context) {
                      myRecorder.objects.context = new (
                              window.AudioContext || window.webkitAudioContext
                              );
                  }
              },
              start: function () {
                  var options = {audio: true, video: false};
                  navigator.mediaDevices.getUserMedia(options).then(function (stream) {
                      myRecorder.objects.stream = stream;
                      myRecorder.objects.recorder = new Recorder(
                              myRecorder.objects.context.createMediaStreamSource(stream),
                              {numChannels: 1}
                      );
                      myRecorder.objects.recorder.record();
                  }).catch(function (err) {});
              },
              stop: function (listObject) {
                  if (null !== myRecorder.objects.stream) {
                      myRecorder.objects.stream.getAudioTracks()[0].stop();
                  }
                  if (null !== myRecorder.objects.recorder) {
                      myRecorder.objects.recorder.stop();

                      if (null !== listObject
                              && 'object' === typeof listObject
                              && listObject.length > 0) {

                          myRecorder.objects.recorder.exportWAV(function (blob) {
                              var url = (window.URL || window.webkitURL)
                                      .createObjectURL(blob);

                              var audioObject = $('<audio controls></audio>')
                                      .attr('src', url);

                              var downloadObject = $('<a>Use</a>')
                                      .attr('href', url)
                                      .attr('download', new Date().toUTCString() + '.wav');


                              var holderObject = $('<div class="row"></div>')
                                      .append(audioObject)
                                      .append(downloadObject);

                              listObject.append(holderObject);
                          });
                      }
                  }
              }
          };

          var listObject = $('[data-role="recordings"]');

          $('[data-role="controls"] > button').click(function () {

              myRecorder.init();

              var buttonState = !!$(this).attr('data-recording');

              if (!buttonState) {
                  $(this).attr('data-recording', 'true');
                  myRecorder.start();
              } else {
                  $(this).attr('data-recording', '');
                  myRecorder.stop(listObject);
              }
          });
      });
