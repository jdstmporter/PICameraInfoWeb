import re

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

    @classmethod
    def path(cls, string):
        try:
            return re.match('^/?(.*)$',string).groups()[0]
        except:
            return '????'

    def __call__(self, environ, start_response):
        path = WSGIApp.path(environ['PATH_INFO'])

        if len(path) == 0:
            responder = ResponseObject(status='200 OK',
                                       contentType='application/json',
                                       text=self.json.encode('utf-8'))
        else:
            responder = ResponseObject(status='404 Not Found',
                                       text=b'NotFound')

        responder(start_response)
        return responder.text

