import os
import ftplib


FTP_URL = 'localhost'
username = 'admin'
password = '123'


ftp = ftplib.FTP(FTP_URL, username, password)

print("File List:", end=' ')
files = ftp.dir()
print(files)

#ftp.cwd("folderOne/subFolder") Change Working Directory

listing = []
ftp.retrlines("LIST", listing.append)
words = listing[0].split(None, 8)
print('words', words)
filename = words[-1]
print(filename)

local_filename = 'ftp/'+ filename


gFile = open(local_filename, 'wb')
ftp.retrbinary(local_filename, gFile.write)
gFile.close()