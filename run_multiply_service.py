from ThriftApp.Server import Server

if __name__ == '__main__':
    server = Server()
    server.run(host='localhost', port='5051')