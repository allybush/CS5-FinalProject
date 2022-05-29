function getSongData(url) {
    console.log(url);
    console.log('here!!');

    if(document.getElementById('innerdecision') != null)
    {
      document.getElementById('innerdecision').remove();
    }
    var name = "url";
    var param = name + "=" + url;
    var xhttp = new XMLHttpRequest();

    xhttp.open('POST', '/song', true);
    xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

    xhttp.onreadystatechange = function() { //Call a function when the state changes.
      if(xhttp.readyState == 4 && xhttp.status == 200) {
          var div = document.getElementById("decision");
          var inner = document.createElement("p");
          inner.id = "innerdecision";
          var response = JSON.parse(xhttp.responseText);
          inner.innerHTML = response["result"];
          div.appendChild(inner);
          console.log("done");
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
                  link.onclick = function () { getSongData(response[i]['preview_url'])} ;
                  link.innerHTML = response[i]['name'];
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
       document.getElementById("player").innerHTML="<audio src=\""+soundFile+"\" type=\"audio/wav\" id=\"embed\" loop=\"false\" /> Audio";
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
                  var z = document.getElementById("exit");
                  z.style.display = "block";
                  var y = document.getElementById("use");
                  y.style.display = "block";
                  var t = document.getElementById("text");
                  t.style.display = "block";
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

                              var downloadObject = $('<a>&#9660;</a>')
                                      .attr('href', url)


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
