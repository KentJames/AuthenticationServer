# Creates a command line interface for the server. Parses arguements allowing
# setup as either client or server.
# To do:
#   Refine exception handling
#   Implement multiclient logic.
#   Refine test client/server logic.




import argparse, sys, os
from Server.Protocol import socket_server, socket_client
from Server import exceptions




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

        self.command.add_argument('--testcommand', action = 'store_true', default = False,
                                  help = ('Specifies if client is setup in command port test mode.'))

        self.command.add_argument('--testdata', action = 'store_true', default = False,
                                  help = ('Specifies if client is setup in data port test mode.'))

        # This executes the parse_args method and dumps them into self.args as a namespace.
        
        self.args = self.command.parse_args()
        

    def initialise_ethernet(self):

        if self.args.type=='S':
        
            try: 
                self.ethernetinterface = socket_server.socket_server_command(self.args.HOST,
                                                                           int(self.args.PORT))

            except Exception as msg:

                print(msg)


        elif self.args.type=='C':

            try:

                print("Opening Client in data transfer Mode...")
                self.ethernetinterface = socket_client.socket_client_command(self.args.HOST,int(self.args.PORT))

            except Exception as msg:

                print(msg)

        else:

            raise InvalidArguementException("Rut roh shaggy. Somethings gone wrong...")


    def initialisetestclient(self):

        print("Opening Client in testcommand mode")
        self.ethernetinterface = socket_client.socket_client_command(self.args.HOST,int(self.args.PORT),
                                                                   None, True)



        
        
            



def main():
    cli = servercli()
    


if __name__=="__main__":
    main()

