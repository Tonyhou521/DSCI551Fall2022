import json
import sys
import pandas as pd

def import_json(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
        return data
    

def main():
    data = import_json(sys.argv[1])
    Dic = dict()
    ##for key, value in data.items():
        ##print(key, value)

    for keys,values in data.items():
        for i in values.keys():
            if i == 'S':
                Dic[keys] = str(*values.values())
            ## if its a string set
            if i == 'SS':
                Dic[keys] = list(*values.values())
            if i == 'NS':
                tempList = []
                for k,v in values.items():
                    for each in v:
                        tempList.append(int(*each))
                Dic[keys] = tempList
            if i == 'N':
                Dic[keys] = int(*values.values())

            ## if it's a list
            if i == 'L':
                tempList = []
                for k,v in values.items():
                    for each in v:
                        for eachkey in each.keys():
                            if eachkey == 'S':
                                tempList.append(str(*each.values()))
                            if eachkey == 'N':
                                tempList.append(int(*each.values()))
                            if eachkey == 'SS':
                                tempList.append(list(*each.values()))
                            if eachkey == 'NS':
                                subtempList = []
                                for v2 in values.items():
                                    for each2 in v2:
                                        subtempList.append(int(*each2))
                                tempList.append(subtempList)

                Dic[keys] = tempList
            
            if i =="M":
                tempDic = dict()
                for k,v in values.items():
                    for k1,v1 in v.items():
                        for eachkey in v1.keys():
                            if eachkey == 'N':
                                tempDic[k1] = int(*v1.values())
                            if eachkey == 'S':
                                tempDic[k1] = str(*v1.values())
                

                Dic[keys] = tempDic
                   
    outputname = sys.argv[2]
    with open(outputname, 'w') as f:
        json.dump(Dic, f)
        
            
if __name__ == "__main__":
    main()