'''
Created on Feb 27, 2013

@author: AKIN
'''

import os

def start_server():
    os.system("python ./MMServer/mediaManagerDaemon.py start")
    
    
def stop_server():
    os.system("python ./MMServer/mediaManagerDaemon.py stop")