from google.cloud import vision
import json
import io
import os.path 

def detect_text(path, outputPath, h, w ):
	"""Detects text in the file."""
	dirname = os.path.dirname(__file__)
	client = vision.ImageAnnotatorClient.from_service_account_json(os.path.join(dirname,"..", "visionKey.json"))

	with io.open(path, 'rb') as image_file:
		content = image_file.read()

	jsonPath = os.path.join(dirname, ".." , "data", "template", "form2KeyJson1.json")
	with open(jsonPath) as f:
		json_data = json.load(f)
	
	image = vision.types.Image(content=content)

	response = client.document_text_detection(image=image,image_context={"language_hints": ["en-t-i0-handwrit"]})
	texts = response.text_annotations

	for text in texts:

	   startx = text.bounding_poly.vertices[0].x
	   starty = text.bounding_poly.vertices[0].y
  
	   if(startx < w/2):
		   continue

	   for keyData in json_data['data']:
		   if(starty > (keyData['yMin']*h) and starty <= (keyData['yMax']*h) ):
		      if(keyData['value'] == ""):
		          keyData['value'] = keyData['value'] + text.description
		      else:
		          keyData['value'] = keyData['value'] + " " + text.description
	
	   #print('\n" {} {} {}"'.format(text.description,startx,starty))

   # with open("data/ProcesedImages/rect.json", "w") as outfile: 
	#	outfile.write(json_dumps(json_data)) 

	out_file = open(outputPath, "w") 

	json.dump(json_data, out_file, indent = 6)


	if response.error.message:
		raise Exception(
			'{}\nFor more info on error messages, check: '
			'https://cloud.google.com/apis/design/errors'.format(
				response.error.message))


