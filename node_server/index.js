'use strict';
var express = require('express');
var app = require('express')();
var path = require('path');

app.use(express.static(path.join(__dirname, '')));
app.use(function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
  next();
});
var server = require('http').Server(app);
var io = require('socket.io')(server);
// var cors = require('cors');



server.listen(8080);

app.get('/', function (req, res) {
  console.log("get it?")

  res.sendfile(__dirname + '/index.html');
});

app.get('/test/:room', function (req, res) {
  console.log("below is the room name")
  console.log(room);
  console.log(req.params); //key value pair with room and whatever got passed-in
  console.log(admin.mountpath); // [ '/adm*n', '/manager' ]
  res.sendfile(__dirname + '/index.html');
  res.send('Admin Homepage');
});

app.get('/hello', function (req,res){
  console.log("get it?");
  res.json({ouch:"you hit me"});
})

io.sockets.on('connection', function(socket) {

  // convenience function to log server messages on the client
  function log() {
    var array = ['Message from server:'];
    array.push.apply(array, arguments);
    socket.emit('log', array);
  }

  socket.on('message', function(message) {
    log('Client said: ', message);
    // for a real app, would be room-only (not broadcast)
    socket.broadcast.emit('message', message);
  });

  socket.on('create or join', function(room) {
    log('Received request to create or join room ' + room);

    var numClients = io.sockets.sockets.length;
    log('Room ' + room + ' now has ' + numClients + ' client(s)');

    if (numClients === 1) {
      socket.join(room);
      log('Client ID ' + socket.id + ' created room ' + room);
      socket.emit('created', room, socket.id);

    } else if (numClients === 2) {
      log('Client ID ' + socket.id + ' joined room ' + room);
      io.sockets.in(room).emit('join', room);
      socket.join(room);
      socket.emit('joined', room, socket.id);
      io.sockets.in(room).emit('ready');
    } else { // max two clients
      socket.emit('full', room);
    }
  });

  socket.on('ipaddr', function() {
    var ifaces = os.networkInterfaces();
    for (var dev in ifaces) {
      ifaces[dev].forEach(function(details) {
        if (details.family === 'IPv4' && details.address !== '127.0.0.1') {
          socket.emit('ipaddr', details.address);
        }
      });
    }
  });

  socket.on('bye', function(){
    console.log('received bye');
  });

});
