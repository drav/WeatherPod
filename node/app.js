var port = process.argv[2];

var express = require('express');
var app = express();
var path = require('path');
var lastHumidity;

app.get('/newdata/:temperature/:humidity/:pressure/:altitude', function(req, res) {

  var temperature = req.params.temperature;
  var humidity = req.params.humidity;
  var pressure = req.params.pressure;
  var altitude = req.params.altitude;

  if(humidity == "None") {
    if(lastHumidity) {
      humidity = lastHumidity;
    }

    else {
      humidity = 0;
    }

    var weatherData = {
      "temp": temperature,
      "hum": humidity,
      "pres": pressure,
      "alti": altitude
    };
  }

  else {
    lastHumidity = humidity;

    var weatherData = {
      "temp": temperature,
      "hum": humidity,
      "pres": pressure,
      "alti": altitude
    };
  }

  console.log(weatherData);

  io.emit('weather-data', weatherData)

  res.send("Ok")

})
.get('/', function(req, res) {
  res.render('index.ejs');
})
.use(express.static(path.join(__dirname, '/public')));

var io = require('socket.io')(app.listen(port));

io.on('connection', function(socket) {
  console.log('Someone connected');
});

console.log('Listening on port ' + port);
