
var express = require('express');
var bodyParser = require('body-parser');
var path = require('path');
var app = express();
var morgan = require('morgan');
var fs = require('fs');

app.use(morgan('dev'));

app.use(bodyParser.urlencoded({ extended: true}));
app.use(bodyParser.json());

var port = process.env.PORT || 8080;

// -----------------------------------------------------
app.use(express.static(__dirname));
app.get('/', function(req, res) {
    res.sendFile(path.join(__dirname, "index.html"));
    console.log('got here');
});


// -----------------------------------------------------
app.listen(port);
console.log("up and running on port: 8080");
