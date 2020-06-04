// This file is required by the index.html file and will
// be executed in the renderer process for that window.
// No Node.js APIs are available in this process because
// `nodeIntegration` is turned off. Use `preload.js` to
// selectively enable features needed in the rendering
// process.
'use strict'
//requiring path and fs modules
const path = require('path')
const fs = require('fs')
const processedFolder = '';
//const processedFolder = create
//joining path of directory
//const directoryPath = path.join(__dirname, '../data/ProcesedImages');
        //console.log(directoryPath);

//passsing directoryPath and callback function
function readGivenDirectory(directoryPath){
fs.readdir(directoryPath, function (err, files) {
    
    if (err) {
        return console.log('Unable to scan directory: ' + err);
    }
    document.getElementById("dataTable").style.display="block";
    document.getElementById("display-files").innerHTML = '';
    //listing all files using forEach
    for(var i=0; i<files.length; i++) {
    	var file 		= files[i];
		var fileName 	= isImageFile(file);
		var imgSrc 		= path.join(directoryPath, file);
		if(fileName && isAlignedFile(fileName)){
			document.getElementById("display-files").innerHTML += '<li class"thumb">'+
			'<div style="margin-bottom: 30px;""><div class="displayFullImg"' +
			'onClick=updateMainContent("'+encodeURIComponent(directoryPath)+'","'+encodeURIComponent(file)+'") id="imgThumb_'+fileName+'">'+
			'<img id="img_'+fileName+'" src="'+imgSrc+'"  width="120" height="150" border="3"></div>'+
			'<div>'+file+'</div></div></li>';
		}
	}
});
createSubdirectory(directoryPath);
}

function isImageFile(file){
	//console.log(file);
	var fileArr = file.split('.');
//	console.log(fileArr);
	if (fileArr[1] == 'jpeg' || fileArr[1] == 'jpg' || fileArr[1] == 'png') 
		return fileArr[0];
	else
		return false;
}

function updateMainContent(directoryPath, fileName){
	var decodePath 		= decodeURIComponent(directoryPath);
	var decodeFileName 	= decodeURIComponent(fileName);
	updateMainImage(decodePath, decodeFileName);
	var jsonFile 		= getJsonFileName(decodePath, decodeFileName);
	displayJsonData(jsonFile);
	updateHiddenInput(decodePath, decodeFileName, jsonFile)
}

function getJsonFileName(directoryPath,id){
	var jsonFilePath = path.join(directoryPath, isImageFile(id)+'_QC.json');
	//console.log(jsonFilePath);
	if (fs.existsSync(jsonFilePath)) {
	}else{
		jsonFilePath = path.join(directoryPath, isImageFile(id)+'.json');
	}

	return jsonFilePath;
}

function updateMainImage(directoryPath,id){
	document.getElementById("displaySelected").innerHTML = '<img src="'+directoryPath+'/'+id+'" width="100%" height="100%" border="2"/>'
}

function displayJsonData(jsonFileName){
	var jsonDataAll = getFileData(jsonFileName);
	if(jsonDataAll){
	var jsonData = jsonDataAll.data;
	var isQC = jsonDataAll.qcComplete;
 }
	document.getElementById("submitButton").style.display = "block";
	document.getElementById("displayJson").innerHTML = '';
	var QCState = "Incomplete";
	if(isQC){
		QCState = "Completed";
	}
	updateQCInfo(QCState);


	for(var i=0; i<jsonData.length; i++) {
		var table=jsonData[i];

    	var tableKey = table.Key;
    	var tableValue = table.value;

    	document.getElementById("displayJson").innerHTML += '<div class="setMargin"><label class="inputLabel"><b>'+tableKey+': </b>&nbsp;</label><input id="'+tableKey+'" type="textbox" size="40" value="'+tableValue+'"></div>';
	}
	
}
function updateQCInfo(QCState){
	document.getElementById("QCdivShow").style.display = "block";
	document.getElementById("QCinfo").innerHTML = QCState;
}

function updateHiddenInput(directoryPath, id, jsonFile){
	document.getElementById("imageFilePath").value = path.join(directoryPath, processedFolder, id); 
	document.getElementById("JsonFilePath").value =  path.join(directoryPath, processedFolder, isImageFile(id) + '_QC.json');
}

function getFileData(fileName){
	try {
  		if (fs.existsSync(fileName)) {
  		//	console.log("file exists")
		  }
		else{
  			var dirPathForjson 	= path.join(__dirname, 'data' , 'template', 'form2KeyJson1.json');
  			fileName			= dirPathForjson;
  		}
  		//fileName = "myfile.txt";
  		var data = fs.readFileSync(fileName,'utf8');
		var parsedData = JSON.parse(data);
	} catch(err) {
  		console.log(err)
	}
	//console.log(parsedData);
	return parsedData;
}

function runPython(){
	const spawn = require("child_process").spawn;
	var directory = document.getElementById("directoryFilePath").value;
	console.log(directory);
	const p = path.join(__dirname, "pythonForm", "main.py")
	
	try{
		var pythonProcess = spawn('python3',[p, '-i', directory]);
	
		console.log(pythonProcess);

		pythonProcess.stdout.on('data', (data) => {
			//console.log(data.toString());
			document.getElementById('consoleOutput').innerHTML += '<p>'+data.toString()+'</p>';
			//document.getElementById('consoleOutput').value += '<p>'+data.toString()+'</p>';
			// Do something with the data returned from python script
		});

		pythonProcess.on('error', function(err) {
		  alert('Error occured Executing python: ' + err);
		});
	}catch(err){
		alert("Exception: Occured Executing python "+err)
	}
}

function openQC(){
	const remote = require('electron').remote;
	var mainWindow = remote.getCurrentWindow();
	mainWindow.loadFile('index.html');
}

function openUploadImage(){
	const remote = require('electron').remote;
	var mainWindow = remote.getCurrentWindow();
	mainWindow.loadFile('formUpload.html');
}
function selectDirectory(){
	var filePathName = document.getElementById('selectedDirectory').value;
	if(filePathName){
		readGivenDirectory(filePathName);
	}else{
		alert('Please mention a valid dirctory path name.');
	}
}

function setDirectoryPath(e){
//	console.log(e);
	var directoryPath = getUploadDirectoryPath(e);
	
    console.log(directoryPath);
   // var Folder = path.split("/")
  // console.log(webkitRelativePath);
    
    document.getElementById('selectedDirectory').value = directoryPath;
	//var path = files[0].webkitRelativePath;
}

function getUploadDirectoryPath(e){
	var files = e.target.files;
	//console.log(files);
    var path = files[0].path;
    var directoryPath = path.replace(files[0].name,'');
    return directoryPath;
}
function setUploadedDirectoryPath(e){
	document.getElementById("directoryFilePath").value = getUploadDirectoryPath(e);
}

function saveQCJson(){

	var formElement = document.getElementById("jsonData").elements;
	//console.log(formElement);
	var outJson = new Array();
	for(var i = 0 ; i < formElement.length ; i++){
		var itemObj = new Object();
		var item = formElement.item(i);
		itemObj.Key = item.id;
		itemObj.value = item.value;
		//console.log(item);
		outJson[i] = itemObj; 
        //outJson[item.id] = item.value;
	}
	var obj = new Object();
	//console.log(outJson);
	obj.data = outJson;//JSON.stringify(outJson);
	obj.qcComplete = "True";
	//obj["data"] = outJson;
	//obj["qcComplete"] = "True";
	//var output = JSON.encode(outJson)
	//var obj["data"]= outJson;

	//console.log(obj);
	//console.log(JSON.stringify(outJson));
	var objString = JSON.stringify(obj);
	//console.log(objString);
	

	saveLocally(objString);
	//var filetype = ''
	
}
function saveLocally(obj){
	var files = getFilesPath();
	var imageFilePath = files["imageFilePath"];
	var jsonFilePath = files["jsonFilePath"];
	//var x = document.getElementById("displaySelected").innerHTML;

	//var fileUrl = x.src;
	//console.log(fileUrl);
	//const fs = require('fs');

try { fs.writeFileSync(jsonFilePath, obj, 'utf-8'); }
catch(e) { alert('Failed to save the file !'); }
fileUploadGoogle(jsonFilePath, "jsonFilePath");
fileUploadGoogle(imageFilePath, "imageFilePath");
updateQCInfo("Completed");
alert("Files uploaded on Google Cloud");
}


function getFilesPath(){
//console.log(file);
	var imageFilePath = document.getElementById("imageFilePath").value;
	var jsonFilePath = document.getElementById("JsonFilePath").value;
	var fileArr= new Array();
	fileArr["imageFilePath"] = imageFilePath;
	fileArr["jsonFilePath"] = jsonFilePath;
	return fileArr;

}
function createSubdirectory(directoryPath){
	//var fs = require('fs');
	//var dir = './tmp';
	var folderPath = directoryPath+'/'+processedFolder;

	if (!fs.existsSync(folderPath)){
		fs.mkdirSync(folderPath);
	}
	//const processedFolder = 
}
function isAlignedFile(fileName){
	//var str = "Hello world, welcome to the universe.";
   var n = fileName.includes("_aligned");
   return n;
}
