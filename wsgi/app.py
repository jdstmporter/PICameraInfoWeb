import re
from http import HTTPStatus

from cups import HTTP_STATUS_OK

from data import DataStore


class ResponseObject:

    def __init__(self, status=HTTPStatus.OK, content_type='text/plain', text=''):
        self.status = f'{status.value} {status.phrase}'
        self.headers = [('Content-type', content_type)]
        self.text = [text.encode('utf-8')]

    def __call__(self,respond):
        respond(self.status, self.headers)

class ErrorObject(ResponseObject):

    def __init__(self,status,text=''):
        super().__init__(status=status,text=text)

class DataObject(ResponseObject):
    def __init__(self,json):
        super().__init__(content_type='application/json',text=json)

class WSGIApp:

    def __init__(self, json):
        self.json = json
        self.length = len(json)
        self.datastore = DataStore()

    @classmethod
    def path(cls, string):
        return re.match('^/?(.*)$',string).groups()[0]

    def get_response(self,environ):
        try:
            path = WSGIApp.path(environ['PATH_INFO'])
            if len(path) == 0:
                return DataObject(self.json)
            elif path == 'power':
                info = self.datastore.batteryJSON()
                return DataObject(info)

            else:
                return ErrorObject(status=HTTPStatus.NOT_FOUND,
                                      text='NotFound')

        except Exception as e:
            print(f'Error: {e}')
            return ErrorObject(status=HTTPStatus.INTERNAL_SERVER_ERROR,
                                  text=str(e))

    def __call__(self, environ, start_response):
        responder = self.get_response(environ)
        responder(start_response)
        return responder.text

