import requests
import ftplib

import os
import time
import json
import logging


class Uploader:
    def __init__(self, url, filePath, fileName, verbose=False):
        self.__uploadURL = url + '/' + fileName
        self.__completePath = filePath + '/' + fileName
        self.__verbose = verbose

    def readFile(self):
        if (os.path.isfile(self.__completePath)):
            try:
                self.__file = open(self.__completePath, mode='rb')
                if self.__verbose:
                    print('File read.')
            except Exception as e:
                if self.__verbose:
                    print('ERROR opening local file.', e)
        else:
            self.file = None
            if self.__verbose:
                print('ERROR. File in local path does not exist.')

    def sendData(self):
        try:
            response = requests.post(self.__uploadURL, files={
                'file': self.__file})
            if self.__verbose:
                print('Web server response: {}'.format(response))
        except Exception as e:
            if self.__verbose:
                print('ERROR sending data to web server.', e)
        self.__file.close()

    def deleteFile():
        try:
            os.remove(config['path'])
            if self.__verbose:
                print('Local file deleted')
        except Exception as e:
            print('ERROR.', e)


class FtpReader:
    def __init__(self, host, username, password, verbose=False):
        self.__host = host
        self.__username = username
        self.__password = password
        self.__server = None
        self.__verbose = verbose

    def __getFileName(self):
        listing = []
        self.__server.retrlines('LIST', listing.append)
        if (len(listing) == 0):
            raise Exception('No files available in FTP server')
        words = listing[0].split(None, 8)
        return words[-1]

    def connect(self):
        try:
            self.__server = ftplib.FTP(
                self.__host, self.__username, self.__password)
            if self.__verbose:
                print('Connected to server')
        except Exception as error:
            if self.__verbose:
                print('ERROR connecting to FTP server. ', error)

    def isConnected(self):
        try:
            self.__server.voidcmd('NOOP')
        except Exception as error:
            return False
        return True

    def changeDirectory(self, path):
        try:
            self.__server.cwd(path)
            if self.__verbose:
                    print('Changed directory succesfully')
        except Exception as error:
            if self.__verbose:
                    print('ERROR. Could not change directory, path does not exist.')
        

    def copyFile(self, copyToPath):
        try:
            fileName = self.__getFileName()
            with open(copyToPath, 'wb') as file:
                self.__server.retrbinary('RETR ' + fileName, file.write)
                if self.__verbose:
                    print('File copied')
                return True
        except Exception as error:
            if self.__verbose:
                print('ERROR copying file from FTP server. ', error)
            return False

    def deleteFile(self):
        try:
            fileName = self.__getFileName()
            self.__server.delete(fileName)
            if self.__verbose:
                print('File deleted')
        except Exception as error:
            if self.__verbose:
                print('ERROR deleting file in FTP server. ', error)
            return False
        return True
