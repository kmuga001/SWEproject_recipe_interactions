const http = require('http');
const express = require('express');
const path = require('path');
const app = express();

app.use(express.json());
app.use(express.static("express"));
// default URL for website

function csvToJSArray(data, delimeter) {

  if (delimeter == undefined) 
    delimeter = ',';
  if (delimeter && delimeter.length > 1)
    delimeter = ',';
    console.log("data check:", data);
    
  var newline = '\n';             //newline
  var eof = '';                   //end of file
  var index = 0;                  //index will increment
  var char = data.charAt(index);  //each individual character read
  var row = 0;
  var col = 0;
  var array = new Array();        //return value

  while (char != eof) {//make sure file did not end
      while (char == '\t' || char == '\r' || char == ' ') {//check for tab and spaces
          char = data.charAt(++index); // read next char
      }
    
    var value = "";//value to be incremented
    if (char == '\"') {// value enclosed by double-quotes
      char = data.charAt(++index);
        do {
            if (char != '\"') {// no enclosed quotes and take in normal char
                value += char;// increment value
                char = data.charAt(++index);// move to next char
        }
            if (char == '\"') {// check for escaped double-quote
          var cnext = data.charAt(i+1);
          if (cnext == '\"') {// this is an escaped double-quote. 
            // Add a double-quote to the value, and move two characters ahead.
            value += '\"';
              i += 2;
              char = data.charAt(index);
          }
        }
        }
        while (char != eof && char != '\"');

        if (char == eof) {
        throw "data ended without quote";
      }

        char = data.charAt(++index);
    }
    else {
      // value without quotes
      while (char != eof && char != delimeter && char != newline) {//make sure char is a valid character and not end of file
        value += char; //add char to value
        char = data.charAt(++index); //increment to next char
      }
    }

    // add the value to the array *******
    if (array.length <= row) 
      array.push(new Array());
    array[row].push(value);
    
    // skip whitespaces
    while (char == ' ' || char == '\t' || char == '\r') {
      char = data.charAt(++i);
    }
   

    // go to the next row or column *******
    if (char == delimeter) {
      // to the next column
      col++;
    }
    else if (char == newline) { //******** */
      // to the next row
      col = 0;
      row++;
    }
    else if (char != eof) {
      // unexpected character
      throw "Delimiter expected after character " + i;
    }
    
    // go to the next character
    char = data.charAt(++index);
  } 
  return array;
}

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
    console.log("hello from the search server!");

    var filePath = './test.csv';
    var searchArray = new Array();
    searchArray = csvToJSArray(filePath, ',');
    console.log("array check:", searchArray);

    for(i = 0; i < searchArray.length(); i++){
        for(j = 0; j < searchArray[i].length(); j++){
            if(searchArray[i][j] == "Buff"){
                console.debug("Buff is here");
            } else {
                console.debug("Buff is NOT here");
                break;
            }
        }

    }
    //temp output untill fetch issue is solved. - abel 
    return res.send({
      "array": "array"
  })


});


//

const server = http.createServer(app);
const port = 5000;
server.listen(port);
console.debug('Server listening on port ' + port);
