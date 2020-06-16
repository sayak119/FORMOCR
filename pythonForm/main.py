import cv2
import numpy as np
import math 
import os
import sys, getopt
import azureRecogniser
from shutil import copyfile
import json 
from pdf2image import convert_from_path

dirname = os.path.dirname(__file__)
azureKeyPath = os.path.join(dirname,"..", "credentials.json")
with open(azureKeyPath) as azPath:
        az_data = json.load(azPath)

azure_region = az_data['azure_region']
resource_group = az_data['resource_group']

form_recognizer_endpoint = az_data['form_recognizer_endpoint']
form_recognizer_subscription_key = az_data['form_recognizer_subscription_key']

form_recognizer_model_id_form1 = az_data['form_recognizer_model_id_form1']
form_recognizer_model_id_form2 = az_data['form_recognizer_model_id_form2']


file_type_mapping = {
    "pdf": "application/pdf",
    "png": "image/png",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg"
}

def extractForm2Data(fileName, fileNameWithoutExtension, extension, output_dir_path, formType):
        file_extension = os.path.splitext(fileName)[1][1:].lower()
        if file_extension in ["pdf", "png", "jpg", "jpeg"]:
               file_type = file_type_mapping[file_extension]
               #print("File: {}".format(fileName))
               if formType == "form1": 
                  form_recognizer_model_id = form_recognizer_model_id_form1
               else: 
                  form_recognizer_model_id = form_recognizer_model_id_form2
               extracted_data = azureRecogniser.analyze_form(form_recognizer_endpoint, form_recognizer_subscription_key, form_recognizer_model_id, fileName, file_type)
               outputJsonPath = output_dir_path + fileNameWithoutExtension + '_aligned.json'
               azureRecogniser.extract_key_value_pairs(extracted_data, outputJsonPath, formType)
               alignedImagePath = output_dir_path + fileNameWithoutExtension + '_aligned' + extension
               if file_extension == 'pdf':
                     pages = convert_from_path(fileName)
                     alignedImagePath = output_dir_path + fileNameWithoutExtension + '_aligned' + '.jpeg'
                     for page in pages:
                         page.save(alignedImagePath, 'JPEG')
               else:
                     copyfile(fileName, alignedImagePath) 
        

if __name__ == '__main__':
#	try:
		inputfile = ''
		outputfile = ''
		formtype = ''
		try:
			opts, args = getopt.getopt(sys.argv[1:],"hi:o:t:",["ifile=","ofile=","type="])
		except getopt.GetoptError:
		  	print('main.py -i <inputDirectory> -o <outputDirectory> -t <formType>')
		  	sys.exit(2)
		if not opts:
		  	print('main.py -i <inputDirectory> -o <outputDirectory> -t <formType>')
		  	sys.exit(2)

		for opt, arg in opts:
			if opt == '-h':
				print('main.py -i <inputDirectory> -o <outputDirectory> -t <formType>')
				sys.exit()
			elif opt in ("-i", "--ifile"):
				inputfile = arg
			elif opt in ("-o", "--ofile"):
				outputfile = arg
			elif opt in ("-t", "--type"):
                                formtype = arg
			else:
				print('main.py -i <inputDirectory> -o <outputDirectory> -t <formType>')

		print("Form::: " + str(formtype))
		sys.stdout.flush()
		if os.path.isfile(inputfile):
			print("its a file, not a directory. Input Directory required")
			sys.exit()
		elif formtype == '':
                        print("FormType is mandatory. PossibleValues: form1 or form2")
                        sys.exit()
		else: 
			if outputfile == '':
			   outputfile = inputfile + "output/"
			try:  
			   os.mkdir(outputfile)  
			except OSError as error:  
			   print(error) 
			   sys.exit()

			print('Input Directory path  is: ' +  inputfile + "\n")
			sys.stdout.flush()
			print('Output Directory path is: '  + outputfile + "\n")
			sys.stdout.flush()

			for fileName in os.listdir(inputfile):
			   print("Starting to Process File: " + fileName + "\n")
			   sys.stdout.flush()
			   fileNameWithoutExtension = os.path.splitext(fileName)[0]
			   extension = os.path.splitext(fileName)[1] 
			   if extension == ".png" or extension == ".jpeg" or extension == ".jpg" or extension == ".pdf":
                                   if formtype == "form2" or formtype == "form1":
                                        extractForm2Data(inputfile + fileName,fileNameWithoutExtension, extension, outputfile, formtype) 
                                   else: 
                                        print("Incorrect FormType Value. Possible Values form1 or form2")
                                   print("Completed to Process File:" + fileName + "\n")
                                   sys.stdout.flush()
			   else:
				   print("Filename : " + fileName + " is not a valid Image File. Valid Images are .png, .jpeg, and .jpg \n") 
				   sys.stdout.flush()
			print("####################################################################################################")
			print("############################# Completed Successfully ###############################################")
			print("####################################################################################################")
			sys.stdout.flush()
#	except Exception as e:
#		print("Exception occured in processing the file : " + str(e))  
