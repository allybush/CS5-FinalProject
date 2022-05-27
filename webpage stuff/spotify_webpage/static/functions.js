function getSongData(url) {

    console.log(url);
    console.log('here!!');

    var name = "url";
    var param = name + "=" + url;
    var xhttp = new XMLHttpRequest();

    xhttp.open('POST', '/song', true);
    xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

    xhttp.onreadystatechange = function() {//Call a function when the state changes.
      if(xhttp.readyState == 4 && xhttp.status == 200) {
          var div = document.getElementById("decision");
          var inner = document.createElement("p");
          var response = JSON.parse(xhttp.responseText);
          var text = document.createTextNode(response["result"]);
          inner.appendChild(text);
          div.appendChild(inner);
          $('#spotifyModal').modal('hide');
          console.log("done");
      }
    }
    xhttp.send(param);

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
       var soundFile = "static/"+Math.round(Math.random() * (50 - 1) + 1)+".wav";
       document.getElementById("player").innerHTML="<embed src=\""+soundFile+"\" id=\"embed\" hidden=\"false\" loop=\"false\" />";
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
