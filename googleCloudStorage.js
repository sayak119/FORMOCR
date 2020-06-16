

const {Storage} 	= require('@google-cloud/storage');
var keypath 		= path.join(__dirname,'visionKey.json');
var credentialPath 	= path.join(__dirname,'credentials.json');
const storage 		= new Storage({keyFilename: keypath});

var data = fs.readFileSync(credentialPath,'utf8');
var parsedData = JSON.parse(data);
const bucketName = parsedData['googleBucket'];
const bucket 		= storage.bucket(bucketName);


async function fileUploadGoogle(files) {

	var uploaded = 0;
	for (i = 0; i < files.length; i++) {
		var file = files[i];

		var currDate = new Date();
		var month = currDate.getMonth() + 1;
		var dateFormat = currDate.getFullYear() + '_' + month + '_' + currDate.getDate();
		var filename = path.parse(file.path).base;

		const options = {
			destination: file.formType + '/' + file.type + '/' + dateFormat + '/' + filename
		};

		try{
			var response = await bucket.upload(file.path, options);
			uploaded++;
		}
		catch{
			alert("Failed to upload file to Google Storage. Please check the Key/Internet Connection");
			break;
		}
	}
	if(uploaded == files.length){
		alert("File uploaded successfully to Google Storage");
		updateQCInfo("Completed");
		saveQCJson("Completed", 0);
	}else{
		updateQCInfo("QCComplete-UploadPending",0);
	}
}
