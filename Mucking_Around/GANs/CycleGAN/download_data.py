import requests
import os
import zipfile
from io import StringIO, BytesIO

r = requests.get("https://people.eecs.berkeley.edu/~taesung_park/CycleGAN/datasets/horse2zebra.zip")

r.ok

z = zipfile.ZipFile(BytesIO(r.content))
z.extractall("zebrahorse/")

os.listdir()
