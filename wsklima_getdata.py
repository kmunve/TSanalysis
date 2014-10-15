#!/usr/bin/python

import requests

class wsKlimaRequest():
    
    def __init__(self, method, params=None):
        
        self.wsmethod = method
        self.wsmethods = ['getStationsFromTimeserieTypeElemCodes', 'getMetData']


        if self.wsmethod not in self.wsmethods:
            print "Please choose a valid method:\n"
            for _m in self.wsmethods:
                print _m

        self.params = params
        self.base_url= 'http://eklima.met.no/met/MetService'
        self.wsklima_url = self.base_url

        self._create_wsklima_url()
        
        ### Returns a requests.Response object
#        return requests.get(self.wsklima_url)

        # _r = requests.Request('GET', url=self.base_url, params=self.params) 

        # _d = _r.prepare()
        # _d.url = _d.url.replace('?', self.methods[method])
        
        # _s = requests.Session()
        # self.r = _s.send(_d)


    def _create_wsklima_url(self):

        if self.wsmethod == 'getMetData':
            self.wsklima_url = "{0}?invoke=getMetData&timeserietypeID={1}&format={2}&from={3}&to={4}&stations={5}&elements={6}&hours={7}&months={8}&username={9}".format(self.base_url, self.params['timeserietypeID'], self.params['format'], self.params['from'], self.params['to'], ",".join(map(str, self.params['stations'])), ",".join(map(str, self.params['elements'])), ",".join(map(str, self.params['hours'])), self.params['months'], self.params['username'])
            
            
        else:
            print "Could not create url!"



    def get(self):
        ### Returns a requests.Response object                                                                      
        return requests.get(self.wsklima_url)


def test_getStationsFromTimeserieTypeElemCodes():
    wr = wsKlimaRequest('getStationsFromTimeserieTypeElemCodes', {'timeserietypeID': 2, 'elem_codes': 'FF', 'username': ""})
    print wr.r.text

def test_getMetData():
    wr = wsKlimaRequest('getMetData', {'timeserietypeID': 2, 'format': "", 'from': '2014-01-01', 'to': '2014-01-31', 'stations': [18700,], 'elements': ['ra', 'tam' , 'tax'], 'hours': [0, 6, 12, 18], 'months': "", 'username': ""}).get()
    print wr.text
    print wr.url
 


if __name__ == "__main__":
#    test_getStationsFromTimeserieTypeElemCodes()
    test_getMetData()
        
