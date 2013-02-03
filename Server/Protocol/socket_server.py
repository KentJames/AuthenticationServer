#!/python33

from .. import exceptions
from .framesync import *
from .Authentication import fileservice
import socket,sys,time,pickle


#Define server exceptions:

#Invalid host exception:

class InvalidHost(exceptions.ServerBaseException):
    pass


#Invalid port exception:


class InvalidPort(exceptions.ServerBaseException):
    pass

#I don't know why I put this here?

class ForceClose(exceptions.ServerBaseException):
    pass
    


'''
This is the class which wraps the objects for creating a server for our file transfer tool.

This class is never really expected to be instantiated as a standalone class of its own, 
but through inheritance, in this case with the socket_server_command

'''

class socket_server_data(object):

    def __init__(self,HOST = None,PORT = None,s = None):
        
        
        #Used for buffering data received from socket.
        self.receivedatabuffer = b''

        ####Socket Host and Port####
        self.HOST = HOST
        self.PORTdata = PORT
        #####################


        ####Socket variables####
        self.sd = None

        self.resd = None

        self.afd = None
        self.socktyped = None
        self.protod = None
        self.canonnamed = None
        self.sad = None

        self.connd = None
        self.addrd = None

        #########################



        #Object used for final storage of serialised binary data before being saved with extension received.
        self.datatransfer = None
        
        self.FileInfo={}
        self.ReceivedFile = None

    def connectdatasocket(self):

        print("Attempting to open server data socket")

        for self.resd in socket.getaddrinfo(self.HOST, self.PORTdata, socket.AF_UNSPEC,
                                      socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
            self.afd, self.socktyped, self.protod, self.canonnamed, self.sad = self.resd

            try:
                self.sd = socket.socket(self.afd,self.socktyped,self.protod)
            except socket.error as msg:
                self.sd = None
                continue

            
            try:
                print("Listening for data connection")
                self.sd.bind(self.sad)
                self.sd.listen(0)
            except socket.error as msg:
                self.sd.close()
                self.sd=None
                continue

            

            
        if self.sd is None:
            print("Attempt to open data socket failed")
            raise ForceClose("Something went horribly wrong")
        else:


            print("Listening for data socket connection...")
            self.connd, self.addrd = self.sd.accept()
            print("Successfully Connected to:",self.addrd)
            

    def receivefiledata(self):

        print("Saving to: ", self.FileInfo['Filename'])

        self.datatransfer = None

        while self.datatransfer !=b'':
            
            self.datatransfer = self.connd.recv(BufferSize)
            #print("Received data: ",self.datatransfer)
            self.receivedatabuffer += self.datatransfer



        

    def storedata(self):
        
        
        self.ReceivedFile = open(self.FileInfo['Filename'],'wb+')
        self.ReceivedFile.write(self.receivedatabuffer)
        self.ReceivedFile.close()

        self.receivedatabuffer = b''



    def datasocketcleanup(self):

        ####Socket variables####

        self.resd = None

        self.afd = None
        self.socktyped = None
        self.protod = None
        self.canonnamed = None
        self.sad = None

        self.connd = None
        self.addrd = None

        #########################
        


'''

This class inherits from the data socket server defined above, and this 
is what wraps the protocol variables, which controls the flow of data through the data socket.


The command socket carries all but the raw binary of the object being sent, including the file
extension, the file size and the md5 hash of the file.

It is instantiated through a HOST and PORT and with a set of options which change its behaviour.
'''
        


        

class socket_server_command(socket_server_data):



    def __init__(self,HOST=None,PORTcommand=None,s=None, TestCommand = False):

        #Instantiate data socket.

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

        
        ##Main loop for the server

        while True:
            

            #Incorporate small delay to stop excessive cpu usage.

            time.sleep(0.01)

            #Receive data from client:
            self.data = self.connc.recv(BufferSize)
                
                
                
            #Reflect data back to source to confirm reception.
            self.connc.send(self.data)
            if self.data ==EndSequence:
                print("End data sequence detected. Exiting...")

            elif self.data==ConnectDataSocket:
                    
                    
                        
                self.connectdatasocket()

                    

                        
            elif self.data==TestString:

                #print("Received data:",repr(self.data))
                print("Test sequence detected.")
                    
                    
            elif self.data ==KillSocket:

                print("Terminate Command Socket sequence detected. Exiting...")
                self.connc.close()
                sys.exit(0)
                break

            elif self.data ==SendFileParameters:

                self.receivedictionarypickled = self.connc.recv(BufferSize)
                self.FileInfo = pickle.loads(self.receivedictionarypickled)
                self.connc.send(self.receivedictionarypickled)
                self.parametersreceived = True
                self.receivedictionarypickled = None


            elif self.data ==StartSequence:

                print("Client preparing to transmit data...")

                if self.parametersreceived is not True:

                    raise InvalidFrameSync("Error: File paramters not received from client")

                self.parametersreceived = False
                
                self.receivefiledata()
                self.storedata()
                self.connd.close()


                

                



            elif not self.data:
                print("Client disconnect detected, attempting verification...")
                self.clientdisconnect = True
                break


            else:
                pass
                

            



        
        
        

def main():
    
    socket1 = socket_server_command('192.168.0.7',50006)
#    socket1.listenfortransmission()

    pause = input("Press and key and enter to exit...")


if __name__=="__main__":
    main()


