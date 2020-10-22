const http = require('http');
const express = require('express');
const path = require('path');
const app = express();

app.use(express.json());
app.use(express.static("express"));
// default URL for website

//dependencies for search
const csvparser = require('csv-parser')
const fs = require('fs')

app.get('/response', (req, res) => {
    console.log("hello from server!")
    return res.send({
        "response": "hello from server!"
    })
});

app.use('/', function(req,res){
    res.sendFile(path.join(__dirname+'/index.html'));
    //__dirname : It will resolve to your project folder.
  });

app.get('/search', (req, res) => {
    console.log("hello from the search server!")
    //New code for search
    const dataArray = [];//array storing data set
    fs.createReadStream('interactions_test.csv')//read stream for file
    .pipe(csvparser({}))
    .on('data', (data) => dataArray.push(data))//store all the data in array
    .on('end', () => {
        console.log(dataArray[0]);//for now only output first five recipes
        console.log(dataArray[1]);
        console.log(dataArray[2]);
        console.log(dataArray[3]);
        console.log(dataArray[4]);
    });
    return res.send(dataArray);
});




const server = http.createServer(app);
const port = 3000;
server.listen(port);
console.debug('Server listening on port ' + port);
