#!/usr/bin/env python
import xml2dict
import re
import requests
import json


wr = requests.get(r"http://api01.nve.no/hydrology/forecast/avalanche/v2.0.2/api/AvalancheWarningByRegion/Detail/11/1/2014-12-13/2014-12-14")
print wr.url
print wr.text

d = json.loads(wr.text)

print d, type(d)



