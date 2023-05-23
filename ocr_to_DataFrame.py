# !pip install msrestazure

# pip install azure-cognitiveservices-vision-computervision

import json
import os
import pandas as pd
import time
# import requests
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes, VisualFeatureTypes
from PIL import Image, ImageDraw, ImageFont
# import urllib.request


API_KEY = "<API KEY>"
ENDPOINT = "<END POINT>"
cv_client = ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(API_KEY))

folder_loc = "/content/images"

# Create the pandas DataFrame
df = pd.DataFrame(columns=['Image_name', 'Contents'])

names = []
op_list = []
for files in os.listdir(folder_loc):
  if files.endswith(".jpg"):
    read_image = open(os.path.join (folder_loc, files), "rb")
    print(os.path.join (folder_loc, files))
    names.append(files)


    # # Open the image
    # read_image = open(image_path, "rb")

    # Call API with image and raw response (allows you to get the operation location)
    read_response = cv_client.read_in_stream(read_image, raw=True)
    # Get the operation location (URL with ID as last appendage)
    read_operation_location = read_response.headers["Operation-Location"]
    # Take the ID off and use to get results
    operation_id = read_operation_location.split("/")[-1]

    # Call the "GET" API and wait for the retrieval of the results
    while True:
        read_result = cv_client.get_read_result(operation_id)
        if read_result.status.lower () not in ['notstarted', 'running']:
            break
        print ('Waiting for OCR...')
        time.sleep(0.3)
    op_str = ""
    # Print results, line by line
    if read_result.status == OperationStatusCodes.succeeded:
        for text_result in read_result.analyze_result.read_results:
            for line in text_result.lines:
                output = line.text
                op_str += ' '+output
    # print(op_str)                 #Printing OCR characters
    op_list.append(op_str)
    print ('OCR Done...')
                # print(line.bounding_box)
df.Image_name = names                    #Making a dataframe with ocr information ''' column 1: image name'''
df.Contents = op_list                    #Making a dataframe with ocr information ''' column 2: OCR information '''


