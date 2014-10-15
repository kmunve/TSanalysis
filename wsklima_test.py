import requests
from lxml import etree


"""
Set request parameters. !!! Currently that does not work since the dictionary provides an arbitrary order, but the "invoke" command needs to be send first. 
"""
param = {'timeserietypeID': '2', 'elem_codes': 'FF', 'username': "", 'invoke': 'getStationsFromTimeserieTypeElemCodes'}
#r = requests.get('http://eklima.met.no/met/MetService', params=param)


"""
Current solution with fixed URL string.
"""
#r = requests.get("http://eklima.met.no/met/MetService?invoke=getStationsFromTimeserieTypeElemCodes&timeserietypeID=2&elem_codes=FF&username=")
#r = requests.get("http://eklima.met.no/met/MetService?invoke=getElementsFromTimeserieTypeStation&timeserietypeID=2&stnr=23550")

# r = requests.get("http://eklima.met.no/met/MetService?invoke=getMetData&timeserietypeID=2&format=&from=2006-01-01&to=2006-02-02&stations=18700&elements=ra%2Ctam%2Ctax&hours=0%2C6%2C12%2C18&months=&username=")

r = requests.get("http://eklima.met.no/met/MetService?invoke=getMetData&timeserietypeID=2&format=&from=2013-09-01&to=2014-05-31&stations=18700&elements=ra%2Ctam%2Ctax&hours=0%2C6%2C12%2C18&months=&username=")


print r.url 
print r.text
print r.raw


tree = etree.parse(r.text)

root = tree.getroot()

# Print tree structure of file
print etree.tostring(root, pretty_print=True)


fid = open('blindern_2013-2014.xml', 'w')
fid.write(r.text)
fid.close()
