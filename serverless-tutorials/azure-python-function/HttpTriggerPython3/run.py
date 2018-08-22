import sys, os.path
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'myenv/Lib/site-packages')))

#D:\\home\\site\\wwwroot\\HttpTriggerPython3

import os
import json
import pandas as pd

json_string = '{"name" : "hello world"}'

postreqdata = json.loads(json_string)
response = open('testfile.txt', 'w')
response.write("hello world from "+postreqdata['name'])
response.close()