import datetime as d
import json


def jsonOut(inputList):
    src = inputList[0]['source']
    day = d.datetime.now().strftime('%y%m%d_%H%M%S')
    filename = '{}_{}_output.json'.format(day, src)
    with open('./output/%s'%(filename), 'w') as f:
        json.dump(inputList, f)
        f.close()
    print(filename + ' has been created!')
