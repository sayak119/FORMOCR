
const {Storage} 	= require('@google-cloud/storage');
var keypath 		= path.join(__dirname,'visionKey.json');
const storage 		= new Storage({keyFilename: keypath});
//const bucketName    = 'form2bucket';
const bucketName    = 'sigma-comfort';
const bucket 		= storage.bucket(bucketName);


function fileUploadGoogle(filePath, fileType){ 
	var currDate 	= new Date();
	var month 		= currDate.getMonth()+1;
	var dateFormat 	= currDate.getFullYear()+'_'+month+'_'+currDate.getDate();
	var filename 	= path.parse(filePath).base;
	
	const options = {
		destination : fileType+'/'+dateFormat+'/'+filename
	};

	bucket.upload(filePath, options, function(err, file, apiResponse) {
	if(err){
		alert("File Could not be saved on Google Cloud.");
		return false;
	}
	
	return true;
	  // - "image.png" (with the contents of `/local/path/image.png')
	  // `file` is an instance of a File object that refers to your new file.
	}); 
}
