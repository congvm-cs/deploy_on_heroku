from flask import Flask
from ThriftApp.Server import Server

server = Server()
app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Hello World<h1>'

if __name__ == '__main__':
    server.run(host='0.0.0.0', port='5050')
    app.run(host='0.0.0.0', port='5000')
