import pandas as pd
import sys
import requests
import json

## Writing a query function to query the database and return the Index ID for the cars that are within the price range
def query_from_database(input1, input2):
    print("Retreiving data from database...")
    database_url = 'https://dsci551hw1-2dd6c-default-rtdb.firebaseio.com/cars.json?'
    fillingwords = 'startAt='
    fillingwords1 = 'orderBy="price"&'
    fillingwords2 = '&endAt='
    url = database_url +fillingwords1 +fillingwords + input1 + fillingwords2 + input2
    r = requests.get(url)
    data = r.json()
    key_list = []
    for key in data.keys():
        key_list.append(int(key))
    return key_list

def main():
    user_input_first = sys.argv[1]
    user_input_second = sys.argv[2]
    key_list = query_from_database(user_input_first, user_input_second)
    print("Successfully completed the query with the user's given parameters: {} and {}".format(user_input_first,user_input_second))
    if key_list ==[]:
        print("No car found with the given range!")
    else:
        print("IDs for the car price range are: ")
        print(key_list)

if __name__ == "__main__":
    main()