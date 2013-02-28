'''
Created on Feb 14, 2013

@author: AKIN
'''

import logging

from restclient.restful_lib import Connection

class RosTester:
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.logger = logging.getLogger('Rest Server Tester')
        hdlr = logging.FileHandler('test.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr) 
        self.logger.setLevel(logging.DEBUG)
    
        self._response = ''
        self.jsonRealResponse = {}
        
    def _read_file_into_string(self, fileUrl):
        strResult = ""
        with open(fileUrl) as infile:
            for line in infile:
                strResult += line
        
        return strResult

    def send_request(self, baseUri, requestType, requestCommand, requestHeaders=None, requestBody=None):
        conn = Connection(baseUri)
        self.logger.debug("Connection opened to: " + baseUri)
        
        if requestType == "GET":
            #tmpRealResponse = conn.request_get(strCommand, headers={'Accept':'application/vnd.mediamanager.jbpm+json', 'Content-Type':'application/json'})
            tmpRealResponse = conn.request_get(requestCommand)
            
            for key in tmpRealResponse.keys():
                self.jsonRealResponse[key.encode('ascii','ignore')] = str(tmpRealResponse[key.encode('ascii','ignore')]).encode('ascii','ignore')
            self.logger.debug(str(self.jsonRealResponse['body']))
            pass
        elif requestType == "POST":
            pass
        elif requestType == "PUT":
            pass
        elif requestType == "DELETE":
            conn.request_delete('/items/11232344')
            pass
        
    def check_response(self, expectedResponseFile):
        strExpectedResponse = self._read_file_into_string(expectedResponseFile)
        strExpectedResponse = strExpectedResponse.rstrip()
        self.logger.debug("Real Response: " + str(self.jsonRealResponse))
        if strExpectedResponse == str(self.jsonRealResponse['body']):
            self.logger.debug (strExpectedResponse)
            self.logger.debug("PASSED")
            return "PASSED"
        else:
            self.logger.debug ("Expected body: " + strExpectedResponse)
            self.logger.debug ("Real body: " + str(self.jsonRealResponse['body']))
            self.logger.debug ("FAILED")
            raise AssertionError("Wrong Response")
            return "FAILED"
        
