function getSongData(url) {

    console.log(url);

    if(url == None || url == "None"){
      console.log('KNEW IT!!')
    }


    var xhttp = new XMLHttpRequest();
    // console.log("test!!")
    xhttp.open("POST", `/song`, true);
    xhttp.send();
}
