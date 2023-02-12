__author__ = "Shengtao (Tony) Hou"
__email__ = "shengtao@usc.edu"
__date__ = "09/09/2022"


import requests
import pandas as pd
import sys

json_suffix = '.json'



## first we need to intake the second argument that user input from the command line and store it in a variable

## Based on the filename that they input we have to find the file inside the current directory and load it using read-csv function with pandas

## convert it into dict and use request to upload it to database

def importfile(filename):
    print("Reading filename " + filename)
    inputfile = pd.read_csv(filename)
    print("File successfully uploaded!")
    return inputfile
    
def convert_to_json(dataframe):
    print("Converting dataframe to json...")
    dict = dataframe.to_json(orient='records')
    print("File successfully transformed!")
    return dict

def upload_to_database(filename):
    database_url ='https://dsci551hw1-2dd6c-default-rtdb.firebaseio.com/cars'
    response = requests.put(database_url + json_suffix, data = filename)
    response.text
    response.json()



def main():
    
    user_input_filename = sys.argv[1]
    df = importfile(user_input_filename)
    print(df)
    file_to_upload = convert_to_json(df)
    upload_to_database(file_to_upload)

if __name__ == "__main__":
    main()