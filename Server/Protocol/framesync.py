# Defines binary representations of protocol commands. Do NOT
# alter unless needed.


BufferSize = 65536


TestString = b'TEST'
EndSequence = b'END'
StartSequence = b'START'

KillSocket = b'KILL'
ConnectDataSocket = b'DATACONNECT'
KillDataSocket = b'DATAKILL'

SendFileParameters = b'PARAMETERSSTART'
EndSendFileParameers = b'PARAMETEREND'
