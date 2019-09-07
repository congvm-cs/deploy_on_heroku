import logging
from multiprocessing import Process, Value, Condition
from thrift.server.TServer import TServer
from thrift.transport.TTransport import TTransportException
from time import time

class TModelPoolServer(TServer):
    ''' A server runs a pool of multiple models to serve requests
        Written by CongVm
    '''
    def __init__(self, handler, listModelConfig, *args, logger=None, timeout=0.1, batchSize=1):
        TServer.__init__(self, *args)
        self.timeout = timeout
        self.batchSize = batchSize
        if logger is not None:
            self.logger = logger
        else:
            self.logger = logging.getLogger(__name__)
        self.listModelConfig = listModelConfig
        self.handler = handler
        self.workers = []
        self.isRunning = Value('b', False)
        self.stopCondition = Condition()
        self.postForkCallback = None

    def setPostForkCallback(self, callback):
        if not callable(callback):
            raise TypeError("This is not a callback!")
        self.postForkCallback = callback

    def setListModelConfig(self, listModelConfig):
        """Set the number of worker threads that should be created"""
        self.listModelConfig = listModelConfig

    def workerProcess(self, kwargs):
        """Loop getting clients from the shared queue and process them"""
        # Init Processor here
        self.handlerInstance = self.handler(**kwargs)
        self.procInstance = self.processor(self.handlerInstance)

        if self.postForkCallback:
            self.postForkCallback()

        listClient = []
        t = time()
        while self.isRunning.value:
            try:
                client = self.serverTransport.accept()
                if not client:
                    continue
                listClient.append(client)
                if len(listClient) >= self.batchSize or time() - t >= self.timeout:
                    self.serveClient(self.procInstance, listClient)
                    listClient.clear()
                    t = time()
            except (KeyboardInterrupt, SystemExit):
                return 0
            except Exception as x:
                self.logger.exception(x)

    def parseClients(self, listClient):
        listOtrans = []
        listItrans = []
        listIprot = []
        listOprot = []
        for client in listClient:
            itrans = self.inputTransportFactory.getTransport(client)
            otrans = self.outputTransportFactory.getTransport(client)
            iprot = self.inputProtocolFactory.getProtocol(itrans)
            oprot = self.outputProtocolFactory.getProtocol(otrans)
            listOtrans.append(otrans)
            listItrans.append(itrans)
            listIprot.append(iprot)
            listOprot.append(oprot)
        return listOtrans, listItrans, listIprot, listOprot

    def serveClient(self, procInstance, listClient):
        """Process input/output from a client for as long as possible"""
        listOtrans, listItrans, listIprot, listOprot = self.parseClients(listClient)
        try:
            while True:
                procInstance.process(listIprot, listOprot)
        except TTransportException:
            pass

        except Exception as x:
            self.logger.exception(x)
            for itrans, otrans in zip(listItrans, listOtrans):
                itrans.close()
                otrans.close()

    def serve(self):
        """Start workers and put into queue"""
        # this is a shared state that can tell the workers to exit when False
        self.isRunning.value = True

        # first bind and listen to the port
        self.serverTransport.listen()

        # fork the children
        for modelConfig in self.listModelConfig:
            try:
                w = Process(target=self.workerProcess, args=(modelConfig, ))
                w.daemon = True
                w.start()
                self.workers.append(w)
            except Exception as x:
                self.logger.exception(x)

        # wait until the condition is set by stop()
        while True:
            self.stopCondition.acquire()
            try:
                self.stopCondition.wait()
                break
            except (SystemExit, KeyboardInterrupt):
                break
            except Exception as x:
                self.logger.exception(x)

        self.isRunning.value = False

    def stop(self):
        self.isRunning.value = False
        self.stopCondition.acquire()
        self.stopCondition.notify()
        self.stopCondition.release()
