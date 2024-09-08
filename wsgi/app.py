import re

from data import DataStore


class ResponseObject:
    def __init__(self, status='200 OK', contentType='text/plain', text=b''):
        self.status = status
        self.headers = [('Content-type', contentType)]
        self.text = [text]

    def __call__(self,respond):
        respond(self.status, self.headers)

class WSGIApp:

    def __init__(self, json):
        self.json = json
        self.length = len(json)
        self.datastore = DataStore()

    @classmethod
    def path(cls, string):
        return re.match('^/?(.*)$',string).groups()[0]

    def getResponse(self,environ):
        try:
            path = WSGIApp.path(environ['PATH_INFO'])
            if len(path) == 0:
                return ResponseObject(status='200 OK',
                                      contentType='application/json',
                                      text=self.json.encode('utf-8'))
            elif path == 'power':
                info = self.datastore.batteryJSON()
                return ResponseObject(status='200 OK',
                                      contentType='application/json',
                                      text=info.encode('utf-8'))

            else:
                return ResponseObject(status='404 Not Found',
                                      text=b'NotFound')

        except Exception as e:
            print(f'Error: {e}')
            return ResponseObject(status='500 Internal Server Error',
                                  text=str(e).encode('utf-8'))

    def __call__(self, environ, start_response):
        responder = self.getResponse(environ)
        responder(start_response)
        return responder.text

