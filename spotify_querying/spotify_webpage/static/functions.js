function getSongData(url) {

    console.log(url);
    var xhttp = new XMLHttpRequest();
    // console.log("test!!")
    xhttp.open("POST", `/song`, true);
    xhttp.send();
}
