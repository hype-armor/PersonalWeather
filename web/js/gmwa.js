var getJSON = function(url, callback) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.responseType = 'json';
    xhr.onload = function() {
      var status = xhr.status;
      if (status === 200) {
        callback(null, xhr.response);
      } else {
        callback(status, xhr.response);
      }
    };
    xhr.send();
  };
  document.getElementById("f0").innerHTML = "1";
  getJSON('https://hype-armor-crispy-waffle-rrx5v5rqqrfrr9-5000.preview.app.github.dev/api',
    function(err, data) {
      if (err !== null) {
        document.getElementById("f0").innerHTML = "Error!";
      } else {
        document.getElementById("f0").innerHTML = data.weather.current_conditions.temperature;
      }
    });
  