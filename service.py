import os
import json
import time
from utils import Uploader, FtpReader

config = dict()
configUploader = 'configTest.json'


def setup(filePath, config):
    if (os.path.isfile(filePath)):
        with open(filePath) as file:
            try:
                data = json.load(file)
                for item in data:
                    config[item] = data[item]
            except Exception as error:
                print(error)


def initialize():
    url = config['uploader']['url'] + '/' + config['uploader']['measurement']
    filePath = config['shared']['localFilesPath']
    fileName = config['shared']['localFileName']
    host = config['ftp']['host']
    username = config['ftp']['username']
    password = config['ftp']['password']

    uploader = Uploader(url, filePath, fileName, True)
    ftpReader = FtpReader(host, username, password, True)
    ftpReader.connect()
    ftpReader.changeDirectory(config['ftp']['ftpPath'])
    return (uploader, ftpReader)


def startService():
    global config
    setup(configUploader, config)
    uploader, ftpReader = initialize()
    copyToPath = config['shared']['localFilesPath'] + \
        config['shared']['localFileName']
    fileCopied = None

    while True:
        fileCopied = False

        if not (ftpReader.isConnected()):
            ftpReader.connect()
            if (ftpReader.isConnected()):
                ftpReader.changeDirectory(config['ftp']['ftpPath'])

        if (ftpReader.isConnected()):
            fileCopied = ftpReader.copyFile(copyToPath)
            if (config['ftp']['deleteFile']):
                ftpReader.deleteFile()

        if (fileCopied):
            uploader.readFile()
            uploader.sendData()
            if (config['uploader']['deleteFile']):
                uploader.deleteFile()

        time.sleep(config['shared']['interval'])


startService()
