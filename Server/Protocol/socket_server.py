#!/python33

from .. import exceptions
from .framesync import *
import socket
import sys
import time


class InvalidHost(exceptions.ServerBaseException):
    pass

class InvalidPort(exceptions.ServerBaseException):
    pass

class ForceClose(exceptions.ServerBaseException):
    pass
    




class socket_server_data(object):

    def __init__(self,HOST = None,PORT = None,s = None):
        
        

        self.receivedatabuffer = None

        
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

        self.datatransfer = None

    def connectdatasocket(self):


        for self.resd in socket.getaddrinfo(self.HOST, self.PORTdata, socket.AF_UNSPEC,
                                      socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
            self.afd, self.socktyped, self.protod, self.canonnamed, self.sad = self.resd

            try:
                self.sd = socket.socket(self.afd,self.socktyped,self.protod)
            except socket.error as msg:
                self.sd = None
                continue

            
            try:
                self.sd.bind(self.sad)
                self.sd.listen(1)
            except socket.error as msg:
                self.sd.close()
                self.sd=None
                continue

            

            
        if self.sd is None:
            print("Attempt to open socket failed")
        else:


            print("Listening for socket connection...")
            self.connd, self.addrd = self.sd.accept()
            print("Connected to:",self.addrd)
            self.receivefiledata()

    def receivefiledata(self):

        while True:
            
            self.datatransfer = self.connd.recv(1024)
            self.receiveddatabuffer += self.datatransfer
            if not self.datatransfer:
                self.storedata()
                break
            
        

    def storedata(self):
        pass
        


        

class socket_server_command(socket_server_data):



    def __init__(self,HOST=None,PORTcommand=None,s=None, TestCommand = False):

        socket_server_data.__init__(self)

        

        
        self.HOST = HOST
        self.PORTcommand = PORTcommand
        self.PORTdata = PORTcommand + 1
        self.sc = s
        self.sd = s

        if self.HOST is None:
            raise InvalidHost("Invalid Hostname")

        if self.PORTcommand is None:
            raise InvalidPort("Invalid Port")

        
        
        

        self.resc = None

        self.afc = None
        self.socktypec = None
        self.protoc = None
        self.canonnamec = None
        self.sac = None

        self.connc = None
        self.addrc = None

        self.data = None

        self.clientdisconnect = True


        while self.clientdisconnect is True:

            self.clientdisconnect = None
            self.connectcommandsocket()
            self.listenfortransmission()




    def connectcommandsocket(self):
        
        for self.resc in socket.getaddrinfo(self.HOST, self.PORTcommand, socket.AF_UNSPEC,
                                      socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
            self.afc, self.socktypec, self.protoc, self.canonnamec, self.sac = self.resc

            try:
                self.sc = socket.socket(self.afc,self.socktypec,self.protoc)
            except socket.error as msg:
                self.sc = None
                continue

            
            try:
                print("Trying to open command socket...")
                self.sc.bind(self.sac)
                print("Still trying....")
                self.sc.listen(0)
            except socket.error as msg:
                self.sc.close()
                self.sc=None
                continue

            
        if self.sc is None:
            print("Attempt to open socket failed")
        else:

            try:

                self.connc, self.addrc = self.sc.accept()
                print("Connected to:",self.addrc)
                

            except KeyBoardInterrupt as msg:
                
                raise ForceClose("Force close detected")
                sys.exit(1)


    def listenfortransmission(self):

        while True:
            try:

                #Incorporate small delay to stop excessive cpu usage.

                time.sleep(0.01)

                #Receive data from client:
                self.data = self.connc.recv(1024)
                
                
                
                #Reflect data back to source to confirm reception.
                self.connc.send(self.data)
                if self.data ==b'END':
                    print("End data sequence detected. Exiting...")

                elif self.data==b'DATACONNECT':
                    
                    try:
                        
                        self.connectdatasocket()

                    except socket.error as msg:

                        print(msg)

                        
                elif self.data==b'TEST':
                    print("Received data:",repr(self.data))
                    print("Test sequence detected.")
                    
                    
                elif self.data ==KillSocket:
                    print("Terminate Command Socket sequence detected. Exiting...")
                    self.connc.close()
                    sys.exit(0)
                    break

                elif not self.data:
                    print("Client disconnect detected, attempting verification...")
                    self.clientdisconnect = True
                    break


                else:
                    pass
                

            except:
                print("Socket Closed by client before end sequence transmitted")
                break



        
        
        

def main():
    
    socket1 = socket_server_command('192.168.0.7',50006)
#    socket1.listenfortransmission()

    pause = input("Press and key and enter to exit...")


if __name__=="__main__":
    main()


