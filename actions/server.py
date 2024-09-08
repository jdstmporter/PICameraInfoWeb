from data import DataStore
from wsgi import WSGIApp
from wsgiref.simple_server import make_server

class CameraServer:
    def __init__(self,ip,port):
        self.ip=ip
        self.port=port
        with DataStore() as sql:
            self.info = sql.json()
        print(f'Camera info is : {self.info}')

    def start(self):
        print('Starting server')
        app = WSGIApp(self.info)

        print(f'Serving on port {self.ip}:{self.port}')
        httpd = make_server(self.ip, self.port, app)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print('Interrupt')
            httpd.server_close()