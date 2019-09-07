from flask import Flask
from flask import render_template, request, jsonify
from ThriftApp.Server import Server
from client import MyClient
from client import TPredictResult
from multiprocessing import Process

server = Server()
client = MyClient()
app = Flask(__name__)


@app.route('/predict/', methods=['GET', 'POST'])
def predict():
    # print(request.is_json)
    inputs = request.get_json()
    # print(inputs)
    ret = client.predict(inputs)
    dict_ret = eval(ret.jsonResult)
    return jsonify(dict_ret)


@app.route('/')
def index():
    return render_template("index.html")

# def runFServer(app, host, port):
#     app.debug = True
#     app.run(host, port)

if __name__ == '__main__':
    FServer = Process(target=app.run, args=('192.168.2.120', '5000', ))
    FServer.daemon = True
    FServer.start()

    server.run(host='localhost', port='5050')
    # TServer = Process(target=server.run, args=('0.0.0.0', 5050, ))
    # TServer.daemon=True
    # TServer.start()

    # app.run(host='0.0.0.0', port='5000')
