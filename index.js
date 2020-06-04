'use strict'        
//requiring path and fs modules
const path = require('path')
const fs = require('fs')
//joining path of directory
const directoryPath = path.join(__dirname, 'Documents');
        console.log(directoryPath);
//passsing directoryPath and callback function
fs.readdir(directoryPath, function (err, files) {
    //handling error
    if (err) {
        return console.log('Unable to scan directory: ' + err);
    }
    //listing all files using forEach
    files.forEach(function (file) {
        // Do whatever you want to do with the file
        //console.log(file);
        var para = document.createElement("p");
        var node = document.createTextNode("This is new.");
        para.appendChild(node);
        var element = document.getElementById("div1");
        element.appendChild(para);
    });
});
