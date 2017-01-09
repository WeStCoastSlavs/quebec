function loadResponse() {
      var xhttp = new XMLHttpRequest();
      xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
         document.getElementById("response").innerHTML = this.responseText;
         loadResponse();
        }
      };
      xhttp.open("GET", "webclient", true);
      xhttp.send();
    }
    loadResponse();