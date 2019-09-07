import sys
from thrift.transport import TTransport
from thrift.transport import TSocket
from thrift.transport import TSSLSocket
from thrift.transport import THttpClient
from thrift.protocol import TBinaryProtocol
from ThriftApp.ThriftZMQ.client.ModelServing import Client
from ThriftApp.ThriftZMQ.client.ttypes import *

class MyClient():
    def __init__(self, host='0.0.0.0', port='5050'):
        self.socket = TSocket.TSocket(host, port)
        self.transport = TTransport.TFramedTransport(self.socket)
        self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
        self.client = Client(self.protocol)


    def predict(self, value):
        self.transport.open()
        try:
            ret = self.client.predict(value)
            self.transport.close()
            return ret 
        except Exception as e:
            print(e)
            self.transport.close()
    