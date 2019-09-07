from flask import Flask
from flask import render_template, request, jsonify
from ThriftApp.Server import Server
from client import MyClient
from client import TPredictResult
from multiprocessing import Process

server = Server()
client = MyClient(host='localhost', port='5051')
app = Flask(__name__)


@app.route('/predict/', methods=['GET', 'POST'])
def predict():
    inputs = request.get_json()
    ret = client.predict(inputs)
    dict_ret = eval(ret.jsonResult)
    return jsonify(dict_ret)


@app.route('/')
def index():
    return render_template("index.html")


if __name__ == '__main__':
    FServer = Process(target=app.run, args=('0.0.0.0', '5000', ))
    FServer.daemon = True
    FServer.start()

    server.run(host='localhost', port='5051')
    # TServer = Process(target=server.run, args=('0.0.0.0', 5050, ))
    # TServer.daemon=True
    # TServer.start()

    # app.run(host='0.0.0.0', port='5000')
