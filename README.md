
# FORMOCR

This is a submission for Exact Sciences OCR Hackathon. This code is the source code which can be packaged as linux, MACOS and Windows executable.

## Initial step
1. Create an account on `Google Cloud`.
2. You can go ahead and create a trial account or a full account.
3. After the account creation and verification, create a project.
4. Go to `API & Services` and on the top there will be `Enable APIS and Services`. Click that.
5. Search for Google Vision API and enable it.
6. Search for Google Cloud Storage and enable it (By default, it should be enabled).
7. Create a bucket as told [here](https://cloud.google.com/storage/docs/creating-buckets?authuser=1).
8. Download the credentials json file as told [here](https://cloud.google.com/iam/docs/creating-managing-service-account-keys).
9. Rename the `json` as `visionKey.json`.
10. Get the name of the bucket previously created and put it in the `googleCloudStorage.js` file as shown below.
```javascript
const bucketName = 'ENTER BUCKET NAME HERE';
```

## Starting the Project from The Source Code
1. Install python and Pip  based on the platform - mac/linux/windows.
2. After installation test command `python` and `pip` by in command prompt.
3. In command prompt change directory to package folder - FORMOCR.
4. Run `pip install -r requirment.txt`.
5. Install node and npm.
6. Execute `npm install`.
7. Execute `npm install -g electron-packager`.
8. Launch the UI from the terminal by command `npm start`.
9. For making Linux (Ubuntu), MACOS and Windows executable, run the following commands.
```bash
// For MACOS (tested on MACOS Mojave)
electron-packager . --overwrite --platform=darwin --arch=x64 --icon=./Images/icon.icns --prune=true --out=../release-mac

// For Linux (tested on Ubuntu)
electron-packager . --overwrite --platform=linux --arch=x64 --icon=./Images/icon.icns --prune=true --out=../release-linux

// For Windows (tested on Windows 10)
electron-packager . form-recognizer --overwrite --platform=win32 --arch=x64 --icon=./Images/icon.ico --prune=true --out=../release-win
```

**We have used `python3` for development as `python2.7` has been deprecated. There might be an issue on some systems because in some systems `python3` is called `python` and in some systems it is `python3`.** If the code isn't working and showing `ENOENT` error, then do the following in `renderer.js` file.
```javascript
/* if python3 doesn't work, then replace it with python */
var pythonProcess = spawn('python3',[p, '-i', directory]);
```

## For Linux SetUp 
1. Install python and pip using the link : `https://docs.python-guide.org/starting/install3/linux/`.
2. After installation test command `python` and `pip` by in command prompt.
3. In command prompt change directory to package folder.
4. Run `pip install -r requirment.txt`.

## For Windows Setup
1. Install python from given link. `https://www.python.org/downloads/`.
2. Make sure to select checkbox of `pip` and `Set Environment Variable`.
3. After installation test command `python` and `pip` by in command prompt.
4. Run `pip install -r requirment.txt`.

## For Mac SetUp 
1. Install python  and pip using the link : `https://docs.python-guide.org/starting/install3/osx/`.
2. After installation test command `python` and `pip` by in command prompt.
3. In command prompt change directory to package folder.
4. Run `pip install -r requirment.txt`.
