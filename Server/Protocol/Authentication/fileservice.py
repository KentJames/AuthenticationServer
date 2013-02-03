import sys
import os
from ..Hash import hashob
from ... import exceptions

'''

This Class opens a file and gathers all necessary data about it from the 
operating system which allows it to be sent by socket. This data includes extensions,
expected size, and and md5 hash of the file for authentication purposes.



Refer to the instance of the class as a dictionary to get information about the 
file size, extension, md5 hash, and if it actually exists.

Keys are:

'FileSize' - returns size of file at PATH in bytes
'Exists' - gives boolean output of if PATH is a valid filepath.
'Extension' - gives extension of file at PATH
'md5' - gives md5 hash of file at PATH
'Filename' - Filename at PATH

'''

class FileServiceExcpetion(exceptions.ServerBaseException):
    pass

class fileservice(object):
    
    def __init__(self, PATH):

        self.PATH = PATH
        self.fileinfo = {}

        self.getfiledata()
        

    def __getitem__(self,KEY):

        return str(self.fileinfo[KEY])







    def getfiledata(self):
        
    # Take notes of dictionary keys for referral.

        self.fileinfo.update({'FileSize': os.path.getsize(self.PATH)})
        self.fileinfo.update({'Exists':os.path.exists(self.PATH)})
        self.extension = os.path.splitext(self.PATH)[1]
        self.fileinfo.update({'Extension':self.extension})
        self.filename = os.path.basename(self.PATH)
        self.fileinfo.update({'Filename':self.filename})
        self.hashobj = hashob.hasher_if(self.PATH,'md5')
        self.hashobj.fileaccess()
        self.hashobj.hashtype()
        self.hashobj.hashfile()
        self.md5hash = self.hashobj.returnhexhash()
        self.fileinfo.update({'md5':self.md5hash})
        
            
            





