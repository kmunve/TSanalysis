#!/usr/bin/python
"""
Author: kmunve
"""
import requests

class wsKlimaRequest():
    """
    Creates a request to eklima.met.no using the wsKlima methods.
    See: http://eklima.met.no/wsKlima/start/start_no.html

    Usage: see "test_..." functions at the end of this file.

    """    
    def __init__(self, method, params=None):
        
        self.wsmethod = method
        self.wsmethods = ['getElementsProperties', 'getElementsFromTimeserieType', 'getStationsFromTimeserieTypeElemCodes', 'getMetData']


        if self.wsmethod not in self.wsmethods:
            print "Please choose a valid method:\n"
            for _m in self.wsmethods:
                print _m

        self.params = params
        self.base_url= 'http://eklima.met.no/met/MetService'
        self.wsklima_url = self.base_url

        self._create_wsklima_url()
        

    def _create_wsklima_url(self):

        if self.wsmethod == 'getMetData':
            self.wsklima_url = "{0}?invoke=getMetData&timeserietypeID={1}&format={2}&from={3}&to={4}&stations={5}&elements={6}&hours={7}&months={8}&username={9}".format(self.base_url, self.params['timeserietypeID'], self.params['format'], self.params['from'], self.params['to'], ",".join(map(str, self.params['stations'])), ",".join(map(str, self.params['elements'])), ",".join(map(str, self.params['hours'])), self.params['months'], self.params['username'])
            
        
        elif self.wsmethod == 'getStationsFromTimeserieTypeElemCodes':
            # params = timeserietypeID, elem_codes, username
            self.wsklima_url = "{0}?invoke=getStationsFromTimeserieTypeElemCodes&timeserietypeID={1}&elem_codes={2}&username={3}".format(self.base_url, self.params['timeserietypeID'], ",".join(map(str, self.params['elem_codes'])), self.params['username'])

        elif self.wsmethod == 'getElementsFromTimeserieType':
            # params = timeserietypeID
            self.wsklima_url = "{0}?invoke=getElementsFromTimeserieType&timeserietypeID={1}".format(self.base_url, self.params['timeserietypeID'])
            
        elif self.wsmethod == 'getElementsProperties':
            # params = language, elem_codes
            self.wsklima_url = "{0}?invoke=getElementsProperties&language={1}&elem_codes={2}".format(self.base_url, self.params['language'], ",".join(map(str, self.params['elem_codes'])))


        else:
            print "Could not create url!"



    def get(self):
        ### Returns a requests.Response object                                                                      
        return requests.get(self.wsklima_url)


def test_getStationsFromTimeserieTypeElemCodes():
    wr = wsKlimaRequest('getStationsFromTimeserieTypeElemCodes', {'timeserietypeID': 2, 'elem_codes': ['RR_1', 'RR_24', 'TA', 'UU', 'FF'], 'username': ""}).get()
    print wr.text
    print wr.url

def test_getMetData():
    wr = wsKlimaRequest('getMetData', {'timeserietypeID': 2, 'format': "", 'from': '2014-01-01', 'to': '2014-01-31', 'stations': [18700,], 'elements': ['ra', 'tam' , 'tax'], 'hours': [0, 6, 12, 18], 'months': "", 'username': ""}).get()
    print wr.text
    print wr.url


def test_getElementsFromTimeserieType():
    wr = wsKlimaRequest('getElementsFromTimeserieType', {'timeserietypeID': 2}).get()
    print wr.text
    print wr.url

 


if __name__ == "__main__":
#    test_getStationsFromTimeserieTypeElemCodes()
    test_getElementsFromTimeserieType()
#    test_getMetData()
        
