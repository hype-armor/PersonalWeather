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
  getJSON('https://hype-armor-crispy-waffle-rrx5v5rqqrfrr9-5000.preview.app.github.dev/api',
    function(err, data) {
      if (err !== null) {
        document.getElementById("now_temperature").innerHTML = "Error!";
      } else {
        
        //document.getElementById("now_icon").innerHTML = data.weather.current_conditions.icon;
        document.getElementById("now_temperature").innerHTML = data.weather.current_conditions.feels_like;
        //document.getElementById("now_temperature").innerHTML += data.weather.current_conditions.temperature_unit;
        document.getElementById("nowicon").src = data.weather.current_conditions.icon;
        document.getElementById("now_wind_speed").innerHTML = data.weather.current_conditions.wind_speed;
        document.getElementById("now_wind_direction").innerHTML = data.weather.current_conditions.wind_direction;
        document.getElementById("now_short_forecast").innerHTML = data.weather.current_conditions.short_forecast;

        document.getElementById("1_name").innerHTML = data.forecast.conditions[0].name;
        document.getElementById("1_temperature").innerHTML = data.forecast.conditions[0].feels_like;
        //document.getElementById("1_temperature").innerHTML += data.forecast.conditions[0].temperature_unit;
        document.getElementById("1icon").src = data.forecast.conditions[0].icon;
        document.getElementById("1_wind_speed").innerHTML = data.forecast.conditions[0].wind_speed;
        document.getElementById("1_wind_direction").innerHTML = data.forecast.conditions[0].wind_direction;
        document.getElementById("1_short_forecast").innerHTML = data.forecast.conditions[0].short_forecast;

        document.getElementById("2_name").innerHTML = data.forecast.conditions[1].name;
        document.getElementById("2_temperature").innerHTML = data.forecast.conditions[1].feels_like;
        //document.getElementById("2_temperature").innerHTML += data.forecast.conditions[1].temperature_unit;
        document.getElementById("2icon").src = data.forecast.conditions[1].icon;
        document.getElementById("2_wind_speed").innerHTML = data.forecast.conditions[1].wind_speed;
        document.getElementById("2_wind_direction").innerHTML = data.forecast.conditions[1].wind_direction;
        document.getElementById("2_short_forecast").innerHTML = data.forecast.conditions[1].short_forecast;
      }
    });