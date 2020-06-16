import random
import string
import time
import re
import os
import json
from requests import post as http_post
from requests import delete as http_delete
from requests import get as http_get
import json 
import math


# define function for the form analysis
def analyze_form(form_recognizer_endpoint, form_recognizer_subscription_key, form_recognizer_model_id, file_path, file_type):
    request_url = "{endpoint}/formrecognizer/v2.0-preview/custom/models/{modelId}/analyze".format(
        endpoint = form_recognizer_endpoint,
        modelId  = form_recognizer_model_id
    )   
    headers = {
        'Content-Type': file_type,
        'Ocp-Apim-Subscription-Key': form_recognizer_subscription_key,
    }

    try:
        with open(file_path, "rb") as f:
            data_bytes = f.read()  
        analyze_form_response = http_post(url = request_url, data = data_bytes, headers = headers)

        if analyze_form_response.status_code != 202:
             raise Exception("Analysis of form failed. Got wrong status code: {}. Expected was: 202.".format(
                 analyze_form_response.status_code))
               
        analyze_form_status_url = analyze_form_response.headers["operation-location"]
        while True:
            analyze_form_status_response = http_get(url = analyze_form_status_url, headers = headers)
            analyze_form_status_response_json = analyze_form_status_response.json()
            if analyze_form_status_response.status_code != 200:                    
                raise Exception("Could not analyze form. Status Code: %s. Message:\n%s" %
                                (analyze_form_status_response.status_code, json.dumps(analyze_form_status_response_json, indent=2)))

            analyze_form_status = analyze_form_status_response_json["status"]

            if analyze_form_status == "succeeded":
                return analyze_form_status_response_json         

            if analyze_form_status == "failed":
                raise Exception("Analysis of form failed. Response:\n%s" % json.dumps(analyze_form_status_response_json, indent=2))

            time.sleep(1)
    
    except Exception as e:
        print(str(e))
        raise

def parseTextTogetValue(value, possibleValues):
   #print("Before Value: " + str(value))
   data = value.split(" ")
   i = 0
   validData = []
   invalidData = []
   value = possibleValues[0]
   for temp in data: 
      if(temp == "@" or temp == "." or temp == "B"):
           validData.append(data[i+1])
      elif(temp == "(" or temp == ")" or temp == "O"):
            invalidData.append(data[i+1])
      i = i + 1
   if validData:
   #   print("ValidData" + str(validData))
      value = validData[0]
   else:
   #   print("InvalidData" + str(invalidData))
      final = list(set(possibleValues).difference(invalidData))
      if final:
          value = final[0]
   #print("After Value: " + str(value))
   return value


# extracts the identified key-value pairs into a Pandas dataframe
def extract_key_value_pairs(response, outputFilePath, formType):
    dirname = os.path.dirname(__file__)
    if formType == "form1":
        jsonPath = os.path.join(dirname, ".." , "data", "template", "form1KeyJson1.json")
    else:
        jsonPath = os.path.join(dirname, ".." , "data", "template", "form2KeyJson1.json")
    with open(jsonPath) as f:
        json_data = json.load(f)
    
    map_order = dict()
    for keyData in json_data['data']: 
       map_order[keyData['Key']] = keyData['order']

    if response["status"] == "succeeded":       
        json_data = {}
        data = []
        shippingAddressVal = ""
        billingAddressVal = ""
        shippingCity = ""
        billingCity = ""
 
        for page in response["analyzeResult"]["documentResults"]:
            for key, val in page["fields"].items():
                if val is not None:
                  value = val.get("valueString")
                  confidence = val.get("confidence")
                else:
                  value = ""
                  confidence = ""
                
                if key == "Sex": 
                   possibleValues = [ "Female", "Male"]
                   value = parseTextTogetValue(value, possibleValues)
                if key == "Phone Type":
                   possibleValues = [ "Home", "Mobile", "Work"]
                   value = parseTextTogetValue(value, possibleValues)
                if key == "Type": 
                   possibleValues = ["Private","Medicare", "Medicaid", "Tricare"]
                   value = parseTextTogetValue(value, possibleValues)
                if key == "Relationship":
                   possibleValues  = ["Self", "Spouse", "Other"]
                   value = parseTextTogetValue(value, possibleValues)
                if key == "Latino origin" or key == "Eact Science Insurance":
                   possibleValues = ["Yes", "NO"]
                   value = parseTextTogetValue(value, possibleValues)
                if key == "ICD-10 Code Other" and value == "":
                   value = "Z12.11 and Z12.12"
                if key == "Race":
                   possibleValues = ["White", "Black", "Asian","Native", "American"]
                   value = parseTextTogetValue(value, possibleValues)
                if key == "HealthCare Organisation Name":
                   key = "Organisation Name"
                if key == "Claims Submission Address":
                   key = "Submission Address"
                if key == "Shipping Address":
                   shippingAddressVal = value
                if key == "Billing Address":
                   billingAddressVal = value
                   continue
                if key == "Shipping City State Zip":
                   shippingCity = value
                if key == "Billing City State Zip":
                   billingCity = value
                   continue
                      
                payload = {}
                payload["Key"] = key
                payload["value"] = value
                payload["order"] = map_order[key]
                data.append(payload)
        payload = {}
        payload["Key"] = "formType"
        payload["value"] = formType
        payload["order"] = map_order["formType"]
        data.append(payload)

        if formType == "form1":
            payload = {}
            payload["Key"] = "Billing Address"
            if len(billingAddressVal) != 0:
                payload["value"] = billingAddressVal
            else:   
                payload["value"] = shippingAddressVal
            payload["order"] = map_order["Billing Address"]
            data.append(payload)

            payload = {}
            payload["Key"] = "Billing City State Zip"
            if len(billingAddressVal) != 0:
                payload["value"] = billingCity
            else:
                payload["value"] = shippingCity
            payload["order"] = map_order["Billing City State Zip"]
            data.append(payload)

        data = sorted(data, key=lambda k: k['order'], reverse=False)
        json_data["data"] = data
        with open(outputFilePath, 'w') as outfile:
               json.dump(json_data, outfile)
