'''
Created on Jan 25, 2013

@author: AKIN
'''

import json
import os
import logging

from bottle import get, post, delete, put, run, template, request, response

listResponses = []
indexResponses = 0
maxIndexResponses = 0
responseFilesFolderUrl = ''

def prepare(testSuiteFileUrl, responseFolderUrl):
    # read the response file
    global listResponses
    global indexResponses
    global responseFilesFolderUrl
    global maxIndexResponses
    
    logging.basicConfig(filename='sim.log',level=logging.DEBUG)
    logging.debug('Preparing the server!')
    
    # set global variables
    indexResponses = 0
    responseFilesFolderUrl = responseFolderUrl
    
    if os.path.isfile(testSuiteFileUrl):
        listResponses = [line.strip() for line in open(testSuiteFileUrl)]
        maxIndexResponses = len(listResponses)
        return True
    else:
        # TODO: handle
        print('problem: no file')
        return False

'''
    This method reads the proper response file depending on the response code
    from the file, entity type, and the operation (create, read, update, etc.) 
'''
def readResponseFile(entityType, operationType):    
    global listResponses
    global indexResponses
    global responseFilesFolderUrl
    global maxIndexResponses
    
    if indexResponses >= maxIndexResponses:
        logging.debug('end of the file, should stop')
        return None
    else:
        pass
    
    # build the string for the filename
    strFilename = operationType + '_' + entityType + '_' + listResponses[indexResponses] + '.json'
    
    strFileUrl = responseFilesFolderUrl + '/' + strFilename
    
    fileContent = ''
    
    # read the file content
    if(os.path.isfile(strFileUrl)):
        # this is a file, read
        fileContent = json.load(open(strFileUrl))
        return fileContent
    else:
        # file does not exist, failed
        logging.critical('File does not exist, failed: ' + strFileUrl)  
        return None 

'''
    This method checks if the request headers contain a content-type
    header for "application/json"
'''       
def checkContentType(request):
    # check if the request is with content-type header
    tmpIndex = (request.headers.get('Content-Type')).find('application/json')
    if tmpIndex != -1:
        logging.debug("Content-Type header is correct!")
        return True
    else:
        # TODO Return a proper message!
        logging.critical("Return a proper message! " + request.headers.get('Content-Type'))
        return False

'''
    This method checks if the request has an authorization header.
'''    
def checkAuthorization(request):
    # check if the request is with authentication header
    if request.headers.get('Authorization') != None:
        logging.debug("Authorization header is implemented!")
        return True
    else:
        # TODO Return a proper message!
        logging.debug("Return a proper message!")
        return False  

'''
    This method checks if the request is suitable for temporary
    MM8 implementation.
'''    
def checkMm8Request(request):
    # check if the request is with authentication header
    if request.headers.get('Accept') == 'application/vnd.mediamanager.jbpm+json':
        logging.debug("WARNING! This is required for now.")
        logging.debug("Accept header is received!")
        return True
    else:
        # TODO Return a proper message!
        logging.debug("Return a proper message!")
        return False
          
     
'''
    This is the method that responds to Create command 
'''
@post('/api/types/<entityType>/entities')
def handleCreate(entityType):    
    global indexResponses
    global listResponses
    
    # check headers but they are not really important for read
    if checkAuthorization(request):
        pass
    else:
        response.status = 401
        return "{\"message\": \"authorization required\"}"
        pass
    
    if checkContentType(request):
        pass
    else:
        # this should return 412
        response.status = 412
        logging.debug("{\"message\": \"api.invalidContentType.error\"}")
    
    if checkMm8Request(request):
        pass
    else:
        response.status = 422
        logging.debug("{\"message\":\"Invalid data format: attributes key required\"}")
        pass
    
    dictResponse = readResponseFile(entityType, 'createEntity')
    
    if dictResponse == None:
        # response file not found
        logging.debug('file not found so will return a not-found message')
        response.status = 404
        indexResponses += 1
        return template('<b>CreateEntity called for {{entityType}} but the response file could not be found</b>!', entityType=entityType)
    
    dictResponseHeaders = dictResponse['headers']
    dictResponseBody = dictResponse['body']
    
    # set headers
    for key in dictResponseHeaders.keys():
        response.set_header(key.encode('ascii','ignore'), dictResponseHeaders[key].encode('ascii','ignore'))
    
    newJsonResponse = json.dumps(dictResponseBody)
    
    response.status = int(listResponses[indexResponses])
    
    # finally increase the index
    indexResponses += 1
    
    return newJsonResponse

@delete('/api/types/<entityType>/entities/<entityId>')
def handleDelete(entityType, entityId):
    # TODO: Edit response code: 204
    
    global indexResponses
    global listResponses
    
    # check headers but they are not really important for read
    if checkAuthorization(request):
        pass
    else:
        response.status = 401
        return "{\"message\": \"authorization required\"}"
        pass
    
    if checkContentType(request):
        pass
    else:
        # this is not important for this request
        pass
    
    if checkMm8Request(request):
        pass
    else:
        # this is not important for this request
        pass
    
    dictResponse = readResponseFile(entityType, 'deleteEntity')
    
    if dictResponse == None:
        # response file not found
        logging.debug('file not found so will return a not-found message')
        response.status = 404
        indexResponses += 1
        return template('<b>DeleteEntity called for {{entityType}}:{{entityId}} but the response file could not be found</b>!', entityType=entityType, entityId=entityId)
    
    dictResponseHeaders = dictResponse['headers']
    dictResponseBody = dictResponse['body']
    
    # set headers
    for key in dictResponseHeaders.keys():
        response.set_header(key.encode('ascii','ignore'), dictResponseHeaders[key].encode('ascii','ignore'))
    
    newJsonResponse = json.dumps(dictResponseBody)
    
    response.status = int(listResponses[indexResponses])
    
    # finally increase the index
    indexResponses += 1
    
    return newJsonResponse

@put('/api/types/<entityType>/entities/<entityId>')
def handleEdit(entityType, entityId):
    global indexResponses
    global listResponses
    
    # check headers but they are not really important for read
    if checkAuthorization(request):
        pass
    else:
        response.status = 401
        return "{\"message\": \"authorization required\"}"
        pass
    
    if checkContentType(request):
        pass
    else:
        # this should return 412
        response.status = 412
        return "{\"message\":\"Requests must be made with Content-Type \"application\/json\" header\"}"
    
    if checkMm8Request(request):
        pass
    else:
        response.status = 422
        return "{\"message\":\"Invalid data format: attributes key required\"}"
        pass
    
    dictResponse = readResponseFile(entityType, 'editEntity')
    
    if dictResponse == None:
        # response file not found
        logging.debug('file not found so will return a not-found message')
        response.status = 404
        indexResponses += 1
        return template('<b>CreateEntity called for {{entityType}} but the response file could not be found</b>!', entityType=entityType)
    
    dictResponseHeaders = dictResponse['headers']
    dictResponseBody = dictResponse['body']
    
    # set headers
    for key in dictResponseHeaders.keys():
        response.set_header(key.encode('ascii','ignore'), dictResponseHeaders[key].encode('ascii','ignore'))
    
    newJsonResponse = json.dumps(dictResponseBody)
    
    response.status = int(listResponses[indexResponses])
    
    # finally increase the index
    indexResponses += 1
    
    return newJsonResponse    

@get('/api/types/<entityType>/entities/<entityId>')
def handleGetSingleEntity(entityType, entityId):
    global indexResponses
    global listResponses
    
    # check headers but they are not really important for read
    if checkContentType(request):
        pass
    else:
        pass
    
    if checkMm8Request(request):
        pass
    else:
        pass            
    
    # handle the query parameters
    detached = request.query.detached
    deleted = request.query.deleted
    if detached == "":
        logging.debug("Query Parameter detached is null")
    else:
        logging.debug("Detached:" + detached)
        
    if deleted == "":
        logging.debug("Query Parameter deleted is null")
    else:
        logging.debug("deleted:" + deleted)
    
    dictResponse = readResponseFile(entityType, 'readSingle')
    
    if dictResponse == None:
        # TODO: file not found
        logging.critical('file not found so will return a normal message')
        response.status = 404
        indexResponses += 1
        return template('<b>GetSingleEntity called for {{entityType}}:{{entityId}} but the response file could not be found</b>!', entityType=entityType, entityId=entityId)
    
    dictResponseHeaders = dictResponse['headers']
    dictResponseBody = dictResponse['body']
    
    # set headers
    for key in dictResponseHeaders.keys():
        response.set_header(key.encode('ascii','ignore'), dictResponseHeaders[key].encode('ascii','ignore')) 
    
    newJsonResponse = json.dumps(dictResponseBody)
    
    response.status = int(listResponses[indexResponses])
    
    # finally increase the index
    indexResponses += 1
    
    return newJsonResponse        
    

#if __name__ == '__main__':
def run_simulator():
    
    #if prepare('testSuite.txt', 'C:/Users/Administrator/Documents/GitHub/MMServerStub/MMServer/test'):
    if prepare('testSuite.txt', '/home/smurfs/RobotWorkspace/MMServerStub/MMServer/test'):
        logging.debug('ready to run the server')
    else:
        logging.debug('there is a problem, server will not start')
    
    run(host='localhost', port=6060, debug=True)
    
    logging.debug('server is running')
    
    pass
