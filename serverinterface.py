'''
This particular file:

 Creates a command line interface for the server. Parses arguements allowing
 setup as either client or server.


 File Sending Utility v 0.8.1 , by James Kent <jameschristopherkent@gmail.com>

 This set of objects, and this particular file (acting as a front end command line interface)
 act together to form a point to point file transfer protocol. It's essentially a mirror copy
 of the File Transfer Protocol, but with some authentication as far as what objects are to be
 expected by verification of md5 hashes, and other information about the file.

 At the current time, it has been envisioned as something for use in a raspberry pi hardware data aquisition
 board, that is that data is aquired from an instrument, and this set of objects is invoked to 
 transport the file saved to a remote server via Ethernet. Essentially it is used as part of 
 data aquisition source in comparison to more expensive elements, and allows remote monitoring
 of experiments.

 At the time of this comment block 29/1/2013 , the project is in a very roughly hewn state, exceptions
 require significant clear up but the protocol is beginning to take shape, with the communications protocol
 being tested, and the final protocol being implemented.


 To do:


   Implement serverside logic for conflicting filenames.

   Implement authentication.

   Implement Logging<-- Big one, might require a semi-redesign but useful none the less.




'''






import argparse, sys, os
from Server.Protocol import socket_server, socket_client
from Server import exceptions


'''Define Exceptions:'''



class InvalidArguementException(exceptions.ServerBaseException):
    pass



class ArguementConfliftException(InvalidArguementException):
    pass



class servercli(object):

    def __init__(self):
        
        
        self.args = None
        self.command = None

        self.parse_commandline()

        self.ethernetinterface = None


        if self.args.testcommand is True and self.args.testdata is True:
            raise ArguementConfliftException("You cannot test both data and command at this time.")





        if self.args.testcommand is True:

            #Over-rides if server is selected.
            self.initialisetestclient()

        elif self.args.testdata is True:

            #Requires implementation
            pass

        else:

            self.initialise_ethernet()
           

        
    def parse_commandline(self):

        #Instantiate command line argument parser.

        self.command = argparse.ArgumentParser(description=
                                               'FileTransfer Tool')
        
        # Here we define the arguements to look out for. Unrecognised arguments
        # will raise an exception.
        
        self.command.add_argument('type',metavar = 'Type', default = 'S', choices = ['S','C'],
                             help = ('Specifies which way the tool is setup. '
                                     'S is for server, and C is for client.'))
        
        self.command.add_argument('HOST',metavar = 'H',default = '192.168.0.9',
                             help = ('IP address of server host, '
                                     'default is localhost'))
        
        self.command.add_argument('PORT',metavar = 'P',default = 50006,
                                  help = ('Specifies starting port number used for'
                                          'sockets. PORT is used '
                                          'for command data, and PORT+1 is'
                                          'used for actual data transfer '
                                          'PORTS MUST BE SAME FOR CLIENT AND '
                                          'SERVER. In a later iteration, a'
                                          'version which allows multiple clients'
                                          'is planned'))
        
        self.command.add_argument('MAXUSERS', metavar = 'M', default = 1,
                                   help = ('Specifies maximum number of users for server.'
                                           ' So for 10 users from PORT = 50000, the protocol'
                                           ' will reserve 10 groups of 2 ports (one for'
                                           ' command and the other for data on the'
                                           ' computer) up to port 50020. Server'
                                           ' Mode ONLY.'))

        self.command.add_argument('--filepath', default = None, nargs = 1,
                                  help = ('Specifies file path for the file that the client will send '
                                          'to server.'))
                                                                        

        self.command.add_argument('--testcommand', action = 'store_true', default = False,
                                  help = ('Specifies if client is setup in command port test mode.'))

        self.command.add_argument('--testdata', action = 'store_true', default = False,
                                  help = ('Specifies if client is setup in data port test mode.'))

        # This executes the parse_args method and dumps them into self.args as a namespace.
        
        self.args = self.command.parse_args()


        # Hack thanks to nargs and default not working together, but nothings perfect right.

        if self.args.filepath is None:
            self.args.filepath = [None]
        

    def initialise_ethernet(self):

        #Instantiate client/server dependant upon command line arguements. I am sure there is a more 
        #pythonic way of doing this.

        if self.args.type=='S':
        
             
            self.ethernetinterface = socket_server.socket_server_command(self.args.HOST, int(self.args.PORT))

            

        elif self.args.type=='C':

            try:

                print("Opening Client in data transfer Mode...")
                self.ethernetinterface = socket_client.socket_client_command(self.args.filepath[0], self.args.HOST,int(self.args.PORT))


            #These exceptions should really never happen. 
            except socket_client.InvalidHostClient as msg:

                print(msg)
                sys.exit(1)

            except socket_client.InvalidPortClient as msg:

                print(msg)
                sys.exit(1)



        else:

            raise InvalidArguementException("Rut roh shaggy. Somethings gone wrong...")


    def initialisetestclient(self):

        print("Opening Client in testcommand mode")
        self.ethernetinterface = socket_client.socket_client_command(None, self.args.HOST,int(self.args.PORT),
                                                                   None, True)



        
        
            



def main():
    cli = servercli()
    


if __name__=="__main__":
    main()

