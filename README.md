
# FORMOCR

This is a submission for Exact Sciences OCR Hackathon. This code is the source code which can be packaged as Linux (Ubuntu), macOS and Windows executable.

## Requirement Analysis


## Initial step
1. Create an account on `Google Cloud`.
2. You can go ahead and create a trial account or a full account.
3. After the account creation and verification, create a project.
4. Go to `API & Services` and on the top there will be `Enable APIS and Services`. Click that.
5. Search for Google Cloud Storage and enable it (By default, it should be enabled).
6. Create a bucket as told [here](https://cloud.google.com/storage/docs/creating-buckets?authuser=1).
7. Download the credentials json file as told [here](https://cloud.google.com/iam/docs/creating-managing-service-account-keys).
8. Rename the `json` as `visionKey.json`.
9. Get the name of the bucket previously created and put it in the `googleCloudStorage.js` file as shown below.
```javascript
const bucketName = 'ENTER BUCKET NAME HERE';
```
10. After setting up of Google Cloud account for storage, we setup the form api using Microsoft Azure's [Form Recogniser](https://azure.microsoft.com/en-in/services/cognitive-services/form-recognizer/).
11. Create an account which maybe trial or full-time subscription.
12. As mentioned above, the flexibility of the Azure Form Recogniser system is one of the reason why we chose this. Ypu can [label](https://docs.microsoft.com/en-us/azure/cognitive-services/form-recognizer/quickstarts/label-tool) and create your own dataset which we did for **50** handwritten forms.
13. Create your own `resource group` as mentioned in the Azure Form Recogniser docs.
14. **NOTE - This step is only necessary if you want to retrain the whole system again with a lot more images. Also, adding large number of images, after a certain point won't increase the performance much.** You'll have to setup 2 containers. One for `form-1` and one for `form-2` and label them accordingly.
15. Train as given in the doc [here](https://docs.microsoft.com/en-us/azure/cognitive-services/form-recognizer/quickstarts/label-tool) for each form type and save the **Model ID**.
16. Under your `form recogniser` resource, go to **Pricing Tier** and change it to `Standard`.
17. Under your `form recogniser` resource, go to **Overview** to get `Resource Group`, `Endpoint` and `Location`. The `Location` can be mapped to `Region` [here](https://westus2.dev.cognitive.microsoft.com/docs/services/form-recognizer-api/operations/AnalyzeWithCustomModel). For example, in `eastus.api.cognitive.microsoft.com` the region is `eastus`.
18. Under your `form recogniser` resource, go to **Keys and Endpoint** to get the `Subscription Key`. **Key-1** is used by default.
19. Create a file named `credentials.json` which has the following content.
```json
{
	"azure_region":"region",
	"resource_group" :"resource name",
	"form_recognizer_endpoint" :"endpoint",
	"form_recognizer_subscription_key" :"key",
	"form_recognizer_model_id_form1" : "model ID form-1",
	"form_recognizer_model_id_form2" : "model ID form-2",
	"googleBucket": "google bucket name"

}
```
20. Once the keys are changed, new executables need to be generated again or build from the source for the code to work.

## Starting the Project from The Source Code
1. Install python and Pip  based on the platform - mac/linux/windows.
2. After installation test command `python` and `pip` by in command prompt.
3. In command prompt change directory to package folder - FORMOCR.
4. Run `pip install -r requirment.txt`.
5. Install node and npm.
6. Execute `npm install`.
7. Launch the UI from the terminal by command `npm start`.
8. For making Linux (Ubuntu), macOS and Windows executable, run the following commands.
```bash
// For macOS (tested on macOS Mojave)
npm run package-mac

// For Linux (tested on Ubuntu)
npm run package-linux

// For Windows (tested on Windows 10)
npm run package-win
```

**We have used `python3` for development as `python2.7` has been deprecated. There might be an issue on some systems because in some systems `python3` is called `python` and in some systems it is `python3`.** If the code isn't working and showing `ENOENT` error, then do the following in `renderer.js` file.
```javascript
/* if python3 doesn't work, then replace it with python */
var pythonProcess = spawn('python3',[p, '-i', directory]);
```

## For Ubuntu Setup 
1. Install python and pip using the link : `https://docs.python-guide.org/starting/install3/linux/`.
2. After installation test command `python` and `pip` by in command prompt.
3. In command prompt change directory to package folder.
4. Run `pip install -r requirment.txt`.
5. Run `./formocr` for UI.

## For Windows Setup
1. Install python from given link. `https://www.python.org/downloads/`.
2. Make sure to select checkbox of `pip` and `Set Environment Variable`.
3. After installation test command `python` and `pip` by in command prompt.
4. Run `pip install -r requirment.txt`.
5. Run `formocr.exe` for UI.

## For macOS Setup 
1. Install python  and pip using the link : `https://docs.python-guide.org/starting/install3/osx/`.
2. After installation test command `python` and `pip` by in command prompt.
3. In command prompt change directory to package folder.
4. Run `pip install -r requirment.txt`.
5. Run `formocr` for UI.
