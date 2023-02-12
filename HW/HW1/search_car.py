import pandas as pd
import sys
import requests
import json
from collections import Counter
from itertools import repeat, chain

def lower_case(input):
    input = input.lower()
    ## conver to a series
    input_series = pd.Series(input)
    return input_series


def split_input(input):
    input_list = input.str.split(' |-|\(|\)')
    for i in input_list:
        for eachword in i:
            eachword.strip('')
            if eachword == '':
                i.remove(eachword)
    return input_list

def retrive_data_from_database(input_word):
    quotation_mark = '"'
    database_url = 'https://dsci551hw1-2dd6c-default-rtdb.firebaseio.com/index.json?orderBy="$key"&equalTo='
    url = database_url + quotation_mark + input_word + quotation_mark
    print("URL is: "+ url)
    r = requests.get(url)
    data = r.json()
    value_list = []
    for value in data.values():
        value_list.append(value)
    return value_list

def generate_final_result(input_list):
    sorted_list = list(chain.from_iterable(repeat(i, c) for i,c in Counter(input_list).most_common()))
    ## remove duplicates while maintaining the order
    ## because dictionary keys are unique by defauly so converting our list into a dictionary will remove duplicates automatically.
    result = list(dict.fromkeys(sorted_list))
    return result
        
        


def main():
    user_input_first = sys.argv[1]
    user_input_first_lower = lower_case(user_input_first)
    user_input_list = split_input(user_input_first_lower)
    returned_list = []
    for i in user_input_list:
        for eachword in i:
            print("Retreving data using ({}) as the keyword...".format(eachword))
            data = retrive_data_from_database(eachword)
            ## unnest data
            for eachdata in data:
                for eachvalue in eachdata:
                    returned_list.append(eachvalue)
        if returned_list == []:
            print("No cars found.")
        else:
            result = generate_final_result(returned_list)
            print("IDs of the cars are: ")
            print(result)



if __name__ == "__main__":
    main()