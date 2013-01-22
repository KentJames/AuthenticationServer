# A protocol which defines a client for sending a file to a server using
# one way point to point communication implemented with sockets.

from .. import exceptions
from .framesync import *
from . import fileservice
import socket
import sys

#HOST = '192.168.0.7'                  # The remote host
#PORT = 50006             # The same port as used by the server


#Define Exceptions:

class InvalidHostClient(exceptions.ServerBaseException):
    pass

class InvalidPortClient(exceptions.ServerBaseException):
    pass

class InvalidFrameSync(exceptions.ServerBaseException):
    pass

class FileException(exceptions.ServerBaseException):
    pass

class FilePathException(FileException):
    pass

class FiletypeException(FileException):
    pass






class socket_client_data(object):

    def __init__(self,HOST = None, PORT = None, s = None):

        self.HOST = None
        self.PORTdata = None
        self.sd = None

        self.resd = None

        self.afd = None
        self.socktyped = None
        self.protod = None
        self.canonnamed = None
        self.sad = None

        self.connd = None
        self.addrd = None


        self.FilePath = None
        self.filetosend = None

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



    def opendatasource(self):

            self.filetosend = fileservice.fileservice(self.FilePath)


    def senddata(self):

            pass

    def sendtestsequencedata(self):

        for x in range(10):
            
            try:
           #Attempt to send string...     
                self.sd.send(TestString.encode('utf8'))
                print("Transmitting...")
                self.datareceived = self.sd.recv(1024)   
                print('Received:', data)
                # s.close()
            except AttributeError as msg:
                print(msg)
                self.sd.close()
            except socket.error as msg:
                print(msg)
                raise socket.error("Socket Closed")


        

class socket_client_command(socket_client_data):

    def __init__(self, HOSTclient = None, PORTcommand= None,s = None,
                 TestClientCommand = False, TestClientData = False,FilePath = None):
        

        socket_client_data.__init__(self)

        self.HOST = HOSTclient
        self.PORTcommand = PORTcommand
        self.PORTdata = self.PORTcommand + 1
        self.sc = s
        self.sd = s

        if self.HOST is None:
            raise InvalidHostClient("Invalid Hostname")

        if self.PORTcommand is None:
            raise InvalidPortClient("Invalid Port")

        self.FilePath = FilePath
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
            
            pass

        
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
            print("Socket opened perfectly!")

    def sendtestsequencecommand(self):

        for x in range(10):
            
            try:
           #Attempt to send string...     
                self.sc.send(TestString)
                print("Transmitting...")

                try:

                    self.datareceivedcommand = self.sc.recv(1024)   

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
                self.data = self.sc.recv(1024)
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


    
    

        


       





