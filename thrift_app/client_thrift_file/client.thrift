namespace java ThriftMQ
namespace py ThriftMQ

struct TPredictResult{
        1: i32 errorCode,
        2: string jsonResult,
}

service ModelServing
{
        TPredictResult predict(1: map<string, string> input),
}
