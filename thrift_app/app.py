class Server():
    def __init__(self):
        pass
        
    def run(self):
        from .handler.handler import Model
        from .ThriftZMQ.server.TModelProcessor import Processor
        from .ThriftZMQ.server.TModelPoolServer import TModelPoolServer
        from thrift.transport import TSocket
        from thrift.transport import TTransport
        from thrift.protocol import TBinaryProtocol

        host_ = '0.0.0.0'
        port_ = '8881'

        transport = TSocket.TServerSocket(host=host_, port=port_)
        tfactory = TTransport.TFramedTransportFactory()
        pfactory = TBinaryProtocol.TBinaryProtocolFactory()

        print('========================================')
        print('Multiplication Server')
        print('Host:', host_)
        print('Port:', port_)
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

app = Server()
# server.run()