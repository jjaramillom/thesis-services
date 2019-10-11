import requests
import os
import time
import json

config = {
    "uploadURL": "http://localhost:3000/database/measurement",
    "path": "data",
    "readInterval": 5,
    "deleteFile": False,
    "measurement": "automatic",
    "fileName": "file.csv"
}

configFile = 'config.json'


def setup():
    if (os.path.isfile(configFile)):
        with open(configFile) as file:
            #file = open(configFile)
            try:
                data = json.load(file)
                for item in data:
                    config[item] = data[item] if item in data else config[item]
            except Exception as error:
                print(error)
            


def readFile(path):
    if (os.path.isfile(path)):
        return open(path, mode='rb')
    else:
        raise Exception('ERROR. File in path does not exist.')


def sendData(url, data):
    return requests.post(url, files={'file': data})


setup()

while True:
    try:
        print('Reading file: ', end=' ')
        file = readFile(config['path'] + '/' + config['fileName'])
        print('OK')
        print('Sending file: ', end=' ')
        response = sendData(config['uploadURL'] + '/{}/{}'.format(config['measurement'], config['fileName']), file)
        print('OK')
        file.close()
        if (config["deleteFile"]):
            os.remove(config['path'])
    except Exception as e:
        print('ERROR')
        print(e)
    else:
        print('response: ', response.text)
    print('-----------')
    time.sleep(config['readInterval'])
