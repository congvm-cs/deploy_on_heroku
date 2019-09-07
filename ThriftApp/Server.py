class Server():
    def __init__(self):
        pass
        
    def run(self, host='0.0.0.0', port='5050'):
        from .handler.handler import Model
        from .ThriftZMQ.server.TModelProcessor import Processor
        from .ThriftZMQ.server.TModelPoolServer import TModelPoolServer
        from thrift.transport import TSocket
        from thrift.transport import TTransport
        from thrift.protocol import TBinaryProtocol

        transport = TSocket.TServerSocket(host=host, port=port)
        tfactory = TTransport.TFramedTransportFactory()
        pfactory = TBinaryProtocol.TBinaryProtocolFactory()

        print('========================================')
        print('Multiplication Server')
        print('Host:', host)
        print('Port:', port)
        print('========================================')

        listModelConfig = [{"gpu_id": '-1', 'mem_fraction': 0.2}, 
                        {"gpu_id": '-1', 'mem_fraction': 0.2}]

        server = TModelPoolServer(Model, 
                                listModelConfig,
                                Processor,
                                transport, 
                                tfactory, 
                                pfactory, timeout=0.1, batchSize=10)
        server.serve()

# app = Server()
