__author__ = 'kmunve'

import pandas as pd
import requests
import json
import matplotlib.pyplot as plt

url = 'http://api01.nve.no/hydrology/forecast/avalanche/v2.0.1/api/AvalancheWarningByRegion/Detail/11/1/2014-03-13/2014-03-17'
resp = requests.get(url)
data = json.loads(resp.text)

try:
    print len(data)
    print data[0].keys()

    df = pd.DataFrame(data)
    df['DangerLevel'] = df['DangerLevel'].astype(int)
    df['ValidFrom'] = pd.to_datetime(df['ValidFrom'])
    df['ValidTo'] = pd.to_datetime(df['ValidTo'])
    df['NextWarningTime'] = pd.to_datetime(df['NextWarningTime'])
    df['PublishTime'] = pd.to_datetime(df['PublishTime'])
    df['UtmZone'] = df['UtmZone'].astype(int)
    df['UtmEast'] = df['UtmEast'].astype(int)
    df['UtmNorth'] = df['UtmNorth'].astype(int)
    df['LangKey'] = df['LangKey'].astype(int)
    print df.DangerLevel
    # print df['ValidFrom'], df['DangerLevel']
    # print df.sort(columns='DangerLevel')
    df.to_excel('Lyngen.xlsx', sheet_name='Detail', cols=['DangerLevel', 'ValidFrom'])

except AttributeError:
    print data
    print "Request returned unexpected content!"

print df.AvalancheProblems[0]
df4 = df.query('DangerLevel == 4')

dl_ds = {} # dict of dangerlevel
count = 0
for ap in df4.AvalancheProblems:
    for p in ap:
        if p['DestructiveSizeExtId'] > 2:
            count += 1
    if count > 0:


print "Count = ", count


# df.plot(x='ValidFrom', y='DangerLevel', kind='bar')
# plt.show()
