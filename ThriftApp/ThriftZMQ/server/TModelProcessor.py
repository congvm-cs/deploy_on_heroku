
from thrift.Thrift import TType, TMessageType, TException, TApplicationException
import logging
from .ttypes import *
from thrift.Thrift import TProcessor
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol, TProtocol
try:
    from thrift.protocol import fastbinary
except:
    fastbinary = None


class Iface:
    def predict(self, input):
        """
        Parameters:
         - input
        """
        pass


class Client(Iface):
    def __init__(self, iprot, oprot=None):
        self._iprot = self._oprot = iprot
        if oprot is not None:
            self._oprot = oprot
        self._seqid = 0

    def predict(self, input):
        """
        Parameters:
         - input
        """
        self.send_predict(input)
        return self.recv_predict()

    def send_predict(self, input):
        self._oprot.writeMessageBegin(
            'predict', TMessageType.CALL, self._seqid)
        args = predict_args()
        args.input = input
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_predict(self):
        iprot = self._iprot
        (fname, mtype, rseqid) = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = predict_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        raise TApplicationException(
            TApplicationException.MISSING_RESULT, "predict failed: unknown result")


class Processor(Iface, TProcessor):
    def __init__(self, handler):
        self._handler = handler
        self._processMap = {}
        self._processMap["predict"] = Processor.process_batching_predict

    def process(self, listIprot, listOprot):
        _listSeqId = []
        _listIprot = []
        _listOprot = []
        for iprot, oprot in zip(listIprot, listOprot):
            (name, type, seqid) = iprot.readMessageBegin()
            if name not in self._processMap:
                iprot.skip(TType.STRUCT)
                iprot.readMessageEnd()
                x = TApplicationException(
                    TApplicationException.UNKNOWN_METHOD, 'Unknown function %s' % (name))
                oprot.writeMessageBegin(name, TMessageType.EXCEPTION, seqid)
                x.write(oprot)
                oprot.writeMessageEnd()
                oprot.trans.flush()
                # return
                continue
            _listSeqId.append(seqid)
            _listIprot.append(iprot)
            _listOprot.append(oprot)
        self.process_batching_predict(_listSeqId, _listIprot, _listOprot)
        return True

    def process_batching_predict(self, listSeqid, listIprot, listOprot):
        list_args_input = []
        for seqid, iprot in zip(listSeqid, listIprot):
            args = predict_args()
            args.read(iprot)
            iprot.readMessageEnd()
            list_args_input.append(args.input)

        model_result = self._handler.predict(list_args_input)
        for res, oprot in zip(model_result, listOprot):
            result = predict_result()
            result.success = res
            msg_type = TMessageType.REPLY
            oprot.writeMessageBegin("predict", msg_type, seqid)
            result.write(oprot)
            oprot.writeMessageEnd()
            oprot.trans.flush()

    def process_predict(self, seqid, iprot, oprot):
        args = predict_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = predict_result()
        try:
            result.success = self._handler.predict(args.input)
            msg_type = TMessageType.REPLY
        except (TTransport.TTransportException, KeyboardInterrupt, SystemExit):
            raise
        except Exception as ex:
            msg_type = TMessageType.EXCEPTION
            logging.exception(ex)
            result = TApplicationException(
                TApplicationException.INTERNAL_ERROR, 'Internal error')
        oprot.writeMessageBegin("predict", msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

# HELPER FUNCTIONS AND STRUCTURES


class predict_args:
    """
    Attributes:
     - input
    """

    thrift_spec = (
        None,  # 0
        (1, TType.MAP, 'input', (TType.STRING, None, TType.STRING, None), None, ),  # 1
    )

    def __init__(self, input=None,):
        self.input = input

    def read(self, iprot):
        if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
            fastbinary.decode_binary(
                self, iprot.trans, (self.__class__, self.thrift_spec))
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.MAP:
                    self.input = {}
                    (_ktype10, _vtype11, _size9) = iprot.readMapBegin()
                    for _i13 in range(_size9):
                        _key14 = iprot.readString()
                        _val15 = iprot.readString()
                        self.input[_key14] = _val15
                    iprot.readMapEnd()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
            oprot.trans.write(fastbinary.encode_binary(
                self, (self.__class__, self.thrift_spec)))
            return
        oprot.writeStructBegin('predict_args')
        if self.input is not None:
            oprot.writeFieldBegin('input', TType.MAP, 1)
            oprot.writeMapBegin(TType.STRING, TType.STRING, len(self.input))
            for kiter16, viter17 in self.input.items():
                oprot.writeString(kiter16)
                oprot.writeString(viter17)
            oprot.writeMapEnd()
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __hash__(self):
        value = 17
        value = (value * 31) ^ hash(self.input)
        return value

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class predict_result:
    """
    Attributes:
     - success
    """

    thrift_spec = (
        (0, TType.STRUCT, 'success', (TPredictResult,
                                      TPredictResult.thrift_spec), None, ),  # 0
    )

    def __init__(self, success=None,):
        self.success = success

    def read(self, iprot):
        if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
            fastbinary.decode_binary(
                self, iprot.trans, (self.__class__, self.thrift_spec))
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 0:
                if ftype == TType.STRUCT:
                    self.success = TPredictResult()
                    self.success.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
            oprot.trans.write(fastbinary.encode_binary(
                self, (self.__class__, self.thrift_spec)))
            return
        oprot.writeStructBegin('predict_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.STRUCT, 0)
            self.success.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __hash__(self):
        value = 17
        value = (value * 31) ^ hash(self.success)
        return value

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)
