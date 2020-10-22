const http = require('http');
const express = require('express');
const path = require('path');
const app = express();

//Testing for search. Necessary dependencies
const fs = require('fs')
const csv = require('csvtojson')//read file

/*(async () => {
    const recipeValues = csv().fromFile('interactions_test.csv')//load data
    console.log(recipeValues)//outputs data

})();
//end testing*/

app.use(express.json());
app.use(express.static("express"));
// default URL for website

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
    const recipeValues = csv().fromFile('interactions_test.csv')//load data
    console.log(recipeValues)//outputs data
    
    return res.send(recipeValues);
});




const server = http.createServer(app);
const port = 3000;
server.listen(port);
console.debug('Server listening on port ' + port);