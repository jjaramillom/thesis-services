import os
import ftplib
import time
import json

config = {
    "host": "192.168.1.3",
    "username": "ELAU",
    "password": "acx35eikl",
    "ftpPath": "ram0:",
    "localPath": "files/",
    "localFileName": "temp.csv",
    "readInterval": 5,
    "deleteFile": False
}

configFile = 'configFTP.json'


def setup():
    if (os.path.isfile(configFile)):
        with open(configFile) as file:
            try:
                data = json.load(file)
                for item in data:
                    config[item] = data[item] if item in data else config[item]
            except Exception as error:
                print(error)


def connectToServer(host, username, password):
    try:
        server = ftplib.FTP(host, username, password)
    except Exception as error:
        print('ERROR connecting. ', error)
        return False
    return server


def getFileName(path):
    global server
    server.cwd(path)  # Change Working Directory
    listing = []
    server.retrlines("LIST", listing.append)
    if (len(listing) == 0):
        raise Exception('No files available')
    words = listing[0].split(None, 8)
    return words[-1]


def deleteFile(fileName):
    global server
    try:
        server.delete(filename)
    except Exception as error:
        print('ERROR. ', error)
        return False
    return True
    


def isConnected():
    global server
    try:
        server.voidcmd("NOOP")
    except Exception as error:
        return False
    return True


def init():
    global server
    if (server):
        print('Connected to server')
        server.cwd(config['ftpPath'])
    while True:
        if not (isConnected()):
            server = connectToServer(config['host'], config['username'], config['password'])
            if (isConnected()):
                server.cwd(config['ftpPath'])
        
        if (isConnected()):
            try:
                fileName = getFileName(config['ftpPath'])
                with open(config['localFileName'], "wb") as file: 
                    server.retrbinary("RETR " + fileName, file.write)
                    print('File copied locally.')
            except Exception as error:
                print('ERROR. ', error)
            
            if (config['deleteFile']):
                try:
                    deleteFile(fileName)
                    print('File deleted in FTP server.')
                except Exception as error:
                    print('ERROR. ', error)
        else :
        print('-----------')
        time.sleep(config['readInterval'])


setup()
server = connectToServer(config['host'], config['username'], config['password'])
init()