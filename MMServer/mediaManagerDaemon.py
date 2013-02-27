'''
Created on Feb 14, 2013

@author: smurfs
'''

# To kick off the script, run the following from the python directory:
#   PYTHONPATH=`pwd` python testdaemon.py start

#standard python libs
import logging
import time
import json
import os

#third party libs
from daemon import runner
from config import config
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
    
    logging.basicConfig(filename='/home/smurfs/sim.log',level=logging.DEBUG)
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
        logger.debug('end of the file, should stop')
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
        logger.critical('File does not exist, failed: ' + strFileUrl)  
        return None 

'''
    This method checks if the request headers contain a content-type
    header for "application/json"
'''       
def checkContentType(request):
    # check if the request is with content-type header
    tmpIndex = (request.headers.get('Content-Type')).find('application/json')
    if tmpIndex != -1:
        logger.debug("Content-Type header is correct!")
        return True
    else:
        # TODO Return a proper message!
        logger.critical("Return a proper message! " + request.headers.get('Content-Type'))
        return False

'''
    This method checks if the request has an authorization header.
'''    
def checkAuthorization(request):
    # check if the request is with authentication header
    if request.headers.get('Authorization') != None:
        logger.debug("Authorization header is implemented!")
        return True
    else:
        # TODO Return a proper message!
        logger.debug("Return a proper message!")
        return False  

'''
    This method checks if the request is suitable for temporary
    MM8 implementation.
'''    
def checkMm8Request(request):
    # check if the request is with authentication header
    if request.headers.get('Accept') == 'application/vnd.mediamanager.jbpm+json':
        logger.debug("WARNING! This is required for now.")
        logger.debug("Accept header is received!")
        return True
    else:
        # TODO Return a proper message!
        logger.debug("Return a proper message!")
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
        logger.debug("{\"message\": \"api.invalidContentType.error\"}")
    
    if checkMm8Request(request):
        pass
    else:
        response.status = 422
        logger.debug("{\"message\":\"Invalid data format: attributes key required\"}")
        pass
    
    dictResponse = readResponseFile(entityType, 'createEntity')
    
    if dictResponse == None:
        # response file not found
        logger.debug('file not found so will return a not-found message')
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
        logger.debug('file not found so will return a not-found message')
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
        logger.debug('file not found so will return a not-found message')
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
    
    logging.debug('get entity called!')
    logging.debug('indexResponses: ' + str(indexResponses))
    logging.debug('listResponses' + str(listResponses))
    logging.debug('')
    
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
        logger.debug("Query Parameter detached is null")
    else:
        logger.debug("Detached:" + detached)
        
    if deleted == "":
        logger.debug("Query Parameter deleted is null")
    else:
        logger.debug("deleted:" + deleted)
    
    dictResponse = readResponseFile(entityType, 'readSingle')
    
    if dictResponse == None:
        # TODO: file not found
        logger.critical('file not found so will return a normal message')
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
def run_simulator():

    #if prepare('testSuite.txt', 'C:/Users/Administrator/Documents/GitHub/MMServerStub/MMServer/test'):
    if prepare(config['TestSuiteFilePath'], config['ResponseFolderPath']):
        logger.debug('ready to run the server')
    else:
        logger.debug('there is a problem, server will not start')
    
    run(host='localhost', port=6060, debug=True)
    
    logger.debug('server is running')
    
    pass

class App():
   
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path =  '/tmp/testdaemon.pid'
        self.pidfile_timeout = 5
           
    def run(self):
        run_simulator()
        while True:
            #Main code goes here ...
            #Note that logger level needs to be set to logger.DEBUG before this shows up in the logs
            logger.debug("Debug message")
            logger.info("Info message")
            logger.warn("Warning message")
            logger.error("Error message")
            time.sleep(10)

app = App()
logger = logging.getLogger("DaemonLog")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.FileHandler("/home/smurfs/testdaemon.log")
handler.setFormatter(formatter)
logger.addHandler(handler)

daemon_runner = runner.DaemonRunner(app)
#This ensures that the logger file handle does not get closed during daemonization
daemon_runner.daemon_context.files_preserve=[handler.stream]
daemon_runner.do_action()
