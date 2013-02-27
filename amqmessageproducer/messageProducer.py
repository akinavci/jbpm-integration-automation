'''
Created on Jan 29, 2013

@author: AKINAVCI
'''
from stompest.config import StompConfig
from stompest.sync import Stomp
import logging

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

# TODO: Read from config file....
CONFIG = StompConfig("tcp://localhost:61613")
#QUEUE = "pods2jbpm"

def _read_file_into_string(fileUrl):
        strResult = ""
        with open(fileUrl) as infile:
            for line in infile:
                strResult += line
        
        return strResult
    
def send_message(fileUrl, destination=None, queueName=None):
    
    fileContent = _read_file_into_string(fileUrl)
    
    client = None
    if destination != None:
        client = Stomp(StompConfig(destination))
    else:
        client = Stomp(StompConfig("tcp://localhost:61613"))
    
    QUEUE = None
    if queueName != None:
        QUEUE = queueName
    else:
        QUEUE = "pods2jbpm"
        
    #client = Stomp(CONFIG)
    client.connect()
    
    body = fileContent
    
    client.send(QUEUE, body)
    
    client.disconnect()
