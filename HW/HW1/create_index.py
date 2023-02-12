import json
import pandas as pd
import numpy as np
import sys
import requests

json_suffix = '.json'

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)

def importfile(filename):
    print("Reading filename " + filename)
    inputfile = pd.read_csv(filename)
    print("File successfully uploaded!")
    return inputfile

def create_index(df):
    ## extracting keywords from CarName column by splitting the string with space, - and ()
    keywords = df['CarName'].str.split(' |-|\(|\)', expand=False)
    for i in keywords:
        for eachword in i:
            eachword.strip('')
            if eachword == '':
                i.remove(eachword)

    keywords_cleaned = []
    for i in keywords:
        keywords_lower = []
        for eachword in i:
            eachword = eachword.lower()
            keywords_lower.append(eachword)
        keywords_cleaned.append(keywords_lower)

    ##concatenate the keywords_cleaned list into df
    df['keywords'] = keywords_cleaned
    keywords_series = pd.Series(keywords_cleaned)

    ## flatten keywords_series
    keywords_series_flatten = keywords_series.explode()

    ## only keep the unique keywords from keywords_series_flatten  
    keywords_series_flatten_unique = keywords_series_flatten.unique()

    ## for every item in keywords_series_flatten_unique, if it exists in df['keywords'], record the car_ID
    ## create a dictionary with key as keywords and value as car_ID
    keywords_dict = {}
    for i in keywords_series_flatten_unique:
        car_ID = []
        for j in range(len(df['keywords'])):
            if i in df['keywords'][j]:
                car_ID.append(df['car_ID'][j])
        keywords_dict[i] = car_ID

    ## convert keywords_dict into dataframe
    ##keywords_df = pd.DataFrame.from_dict(keywords_dict, orient='index')
    ##keywords_df = keywords_df.reset_index()
    ##keywords_df = keywords_df.rename(columns={'index':'keywords'})
    return keywords_dict

def upload_to_database(filename):
    database_url ='https://dsci551hw1-2dd6c-default-rtdb.firebaseio.com/index'
    response = requests.put(database_url + json_suffix, data = filename)
    response.text
    response.json()

def convert_to_json(inputfile):
    output = json.dumps(inputfile, cls=NpEncoder)
    return output

def main():
    user_input_filename = sys.argv[1]
    df = importfile(user_input_filename)
    keywords = create_index(df)
    file_to_upload = convert_to_json(keywords)
    upload_to_database(file_to_upload)
    print("Done. Check Database to see the imported data")

if __name__ == "__main__":
    main()