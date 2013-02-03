# A protocol which defines a client for sending a file to a server using
# one way point to point communication implemented with sockets.

from .. import exceptions
from .framesync import *
from .Authentication import fileservice
import socket
import sys
import pickle




#Define Exceptions:

#Network Exceptions:

class InvalidHostClient(exceptions.ServerBaseException):
    pass


class InvalidPortClient(exceptions.ServerBaseException):
    pass


class InvalidFrameSync(exceptions.ServerBaseException):
    pass


#I/O Exceptions:

class FileException(exceptions.ServerBaseException):
    pass


class FilePathException(FileException):
    pass


class FiletypeException(FileException):
    pass






class socket_client_data(object):

    def __init__(self,HOST = None, PORT = None, PATH = None, s = None):

        self.HOST = HOST
        self.PORTdata = PORT
        self.sd = None

        self.resd = None

        self.afd = None
        self.socktyped = None
        self.protod = None
        self.canonnamed = None
        self.sad = None

        self.connd = None
        self.addrd = None


        self.FilePath = PATH
        self.filetosend = None
        self.FileInfo = None

        #Used for creating a standalone dictionary for pickling for security reasons.
        self.FileInfoDict = {}

        self.datareceived = None



    def connectdatasocket(self):

        for self.resd in socket.getaddrinfo(self.HOST, self.PORTdata, socket.AF_UNSPEC, socket.SOCK_STREAM):
            self.afd, self.socktyped, self.protod, self.canonnamed, self.sad = self.resd
            
            try:
                self.sd = socket.socket(self.afd, self.socktyped, self.protod)
            except socket.error as msg:
                print(msg)
                self.sd = None
                continue

            try:
                print("Data socket connected to: ",self.sad)
                self.sd.connect(self.sad)
            except socket.error as msg:

                print(msg)
                self.sd.close()
                self.sd = None
                continue
            break


        if self.sd is None:
            raise socket.error("Could not open socket. Check server, or client PORT.")
            #sys.exit(1)

    def openfile(self):
        
        try:

            self.filetosend = open(self.FilePath,'rb')

        except IOError:

            raise FileNotFoundError
        
        except TypeError:

            raise FileNotFoundError



    def getfiledata(self):

        self.FileInfo = fileservice.fileservice(self.FilePath)


        self.FileInfoDict.update({'Extension': self.FileInfo['Extension']})
        self.FileInfoDict.update({'FileSize': self.FileInfo['FileSize']})
        self.FileInfoDict.update({'md5': self.FileInfo['md5']})
        self.FileInfoDict.update({'Filename': self.FileInfo['Filename']})


    def senddata(self):

        self.block = None

        for self.block in iter(lambda: self.filetosend.read(BufferSize),b""):

            #Update the hash algorithm with the bytes we have read
            try:

                self.sd.send(self.block)


            except socket.error:

                print("Why the fuck is this happening?")


        return True




    ##For pinging a servers data socket. Not actually called yet but here just in case.

    def sendtestsequencedata(self):

        for x in range(10):
            
            try:
           #Attempt to send string...     
                self.sd.send(TestString.encode('utf8'))
                print("Transmitting...")
                self.datareceived = self.sd.recv(BufferSize)   
                print('Received:', self.datareceived)
                # s.close()
            except AttributeError as msg:
                print(msg)
                self.sd.close()
            except socket.error as msg:
                print(msg)
                raise socket.error("Socket Closed")


        

class socket_client_command(object):

    def __init__(self,FilePath = None, HOSTclient = None, PORTcommand= None,s = None,
                 TestClientCommand = False, TestClientData = False):
        

        

        self.HOST = HOSTclient
        self.PORTcommand = PORTcommand
        self.PORTdata = self.PORTcommand + 1
        self.sc = s
        

        self.datasocket = None

        if self.HOST is None:
            raise InvalidHostClient("No Hostname specified")

        if self.PORTcommand is None:
            raise InvalidPortClient("No portname specified")

        self.FilePath = FilePath

        #socket_client_data.__init__(self,self.HOST,self.PORTdata,self.FilePath)

        self.TestClientCommand = TestClientCommand

        if self.FilePath is None and self.TestClientCommand==False:
            raise FilePathException("No File Specified to Transmit")

        

        self.resc = None
        self.afc = None
        self.socktypec = None
        self.protoc = None
        self.canonnamec = None
        self.sac = None

        self.connc = None
        self.addrc = None

        self.data = None

        self.connectcommandsocket()

        if self.TestClientCommand is True:

            self.sendtestsequencecommand()
            self.EndTransmission()
            
        else:
            
            self.beginsendingdata()

        
    def connectcommandsocket(self):

        
        for self.resc in socket.getaddrinfo(self.HOST, self.PORTcommand, socket.AF_UNSPEC,
                                            socket.SOCK_STREAM):
            self.afc, self.socktypec, self.protoc, self.canonnamec, self.sac = self.resc
            
            try:
                self.sc = socket.socket(self.afc, self.socktypec, self.protoc)
            except OSError as msg:
                
                self.sc = None
                
                continue
            try:
                self.sc.connect(self.sac)
            except socket.error as msg:
                print(msg)
                self.sc.close()
                self.sc = None
                
                continue
            break


        if self.sc is None:
            raise socket.error("Could not open socket")
            sys.exit(1)
        else:
            print("Command socket connected to: ",self.sac)

    def sendtestsequencecommand(self):

        for x in range(10):
            
            try:
           #Attempt to send string...     
                self.sc.send(TestString)
                print("Transmitting...")

                try:

                    self.datareceivedcommand = self.sc.recv(BufferSize)   

                except WindowsError as msg:

                    print(msg)
                    sys.exit(1)

                    
                print('Received:', self.datareceivedcommand)
                # s.close()
            except AttributeError as msg:
                print(msg)
                self.sc.close()
            except OSError as msg:
                print(msg)

    def EndTransmission(self,HardKill = False):

        self.HardKill = HardKill

        while True:
            

            if self.HardKill is True:

                print("Sending Kill Code...")
                self.sc.send(KillSocket)
                self.data = self.sc.recv(BufferSize)
                if self.data ==KillSocket:

                    #Close data socket.
                    print("Transmission ended successfully!")
                    self.sc.shutdown(socket.SHUT_RDWR)
                    self.sc.close()
                    break
                else:
                    raise socket.error("Transmission did not end successfully!")

            else:

                try:

                    print("Data Transmission ended.")
                    break

                except OSError:

                    print("Closing Socket Problem Occured")




    '''
    The client centrepiece, as it manages the logic for connecting data ports
    and managing the transfer of the raw file data as well as critical information such
    as file extension, md5 hash, and file size.

    '''

    def beginsendingdata(self):

        #Send command to server to connect data socket.

        self.sc.send(ConnectDataSocket)
        self.datareceivedcommand = self.sc.recv(BufferSize)
        #print(self.datareceivedcommand)


        if not self.datareceivedcommand==ConnectDataSocket:
            raise InvalidFrameSync("Server did not respond correctly: socket_client_command.beginsendingdata")
            
        
        #print("Data socket request received by server, attempting to connect to data socket!")

        self.datasocket = socket_client_data(self.HOST, self.PORTdata, self.FilePath)
        #print("Datasocket insantiated")
        self.datasocket.connectdatasocket()
        #print("Data socket connected")


        #Open file and get data about the file.
        self.datasocket.openfile()
        self.datasocket.getfiledata()

        self.sc.send(SendFileParameters)

        self.datareceivedcommand=self.sc.recv(BufferSize)

        if not self.datareceivedcommand==SendFileParameters:
            raise InvalidFrameSync("Server did not respond correctly: socket_client_command.beginsendingdata: SendFileParameters")
        
        self.sc.send(pickle.dumps(self.datasocket.FileInfoDict))
        self.datareceivedcommand = self.sc.recv(BufferSize)

        if not self.datareceivedcommand ==pickle.dumps(self.datasocket.FileInfoDict):

            self.sc.send(KillSocket)
            raise InvalidFrameSync("Server responded incorrectly to pickled data. Connection may be compromised. Kill code engaged.")

        self.sc.send(StartSequence)
        
        self.datareceived = self.sc.recv(BufferSize)

        if not self.datareceived ==StartSequence:
            raise InvalidFrameSync("StartSequence byte not repeated")

        self.datasocket.senddata()

        #Close data socket
        self.datasocket.sd.close()








            

            



        ##############
            


    
    

        


       





