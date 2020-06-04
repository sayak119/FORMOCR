import extractBox
import visionAPI
import alignImage

import cv2
import numpy as np
import math 
import os
import sys, getopt

def extractRectAndJson(fileName, fileNameWithoutExtension, output_dir_path):
	im = cv2.imread( fileName, cv2.IMREAD_COLOR)
	dirname = os.path.dirname(__file__)
	templatePath = os.path.join(dirname, ".." , "data", "template", "Form2Template4.png")
	imRef = cv2.imread(templatePath, cv2.IMREAD_COLOR)
	img, h = alignImage.alignImages(im , imRef)
	alignedImagePath = output_dir_path + fileNameWithoutExtension + '_aligned.png'
	cv2.imwrite(alignedImagePath, img)
	image = extractBox.form2rectImage(alignedImagePath)
	h, w = image.shape
	#image=cv2.resize(image,(500,400))

	rectImagePath = output_dir_path + fileNameWithoutExtension + '_rect.png'
	cv2.imwrite(rectImagePath, image)

	outputJsonPath = output_dir_path + fileNameWithoutExtension + '_aligned.json'
	visionAPI.detect_text(rectImagePath, outputJsonPath, h, w)

if __name__ == '__main__':
	try:
		inputfile = ''
		outputfile = ''
		try:
			opts, args = getopt.getopt(sys.argv[1:],"hi:o:",["ifile=","ofile="])
		except getopt.GetoptError:
		  	print('main.py -i <inputDirectory> -o <outputDirectory>')
		  	sys.exit(2)
		if not opts:
		  	print('main.py -i <inputDirectory> -o <outputDirectory>')
		  	sys.exit(2)

		for opt, arg in opts:
			if opt == '-h':
				print('main.py -i <inputDirectory> -o <outputDirectory>')
				sys.exit()
			elif opt in ("-i", "--ifile"):
				inputfile = arg
			elif opt in ("-o", "--ofile"):
				outputfile = arg
			else:
				print('main.py -i <inputDirectory> -o <outputDirectory>')

		if os.path.isfile(inputfile):
			print("its a file, not a directory. Input Directory required")
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
			   if extension == ".png" or extension == ".jpeg" or extension == ".jpg":
				   extractRectAndJson(inputfile + fileName,fileNameWithoutExtension,outputfile)
				   print("Completed to Process File:" + fileName + "\n")
				   sys.stdout.flush()
			   else:
				   print("Filename : " + fileName + " is not a valid Image File. Valid Images are .png, .jpeg, and .jpg \n") 
				   sys.stdout.flush()
	except Exception as e:
		print("Exception occured in processing the file" + str(e))  
