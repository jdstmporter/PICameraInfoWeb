import re
from http import HTTPStatus, HTTPMethod
from collections import defaultdict
from util import Logger

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

class WSGIEnv:

    def __init__(self,env):
        self._env=env

    def __getitem__(self,key):
        return self._env[key]

    def method(self):
        m = self._env['REQUEST_METHOD']
        return HTTPMethod.__members__[m]



    def path(self):
        p = self['PATH_INFO']
        return re.match('^/?(.*)$',p).groups()[0]

    def headers(self):
        out = dict()
        for k ,v in self._env:
            try:
                key = re.match('^HTTP_(\S+)$',k).groups()[0]
                out[key]=v
            except Exception as e:
                Logger.log.error(f'Error getting WSGI headers : {e}')
        return out

    def query(self):
        try:
            queries = self['QUERY_STRING'].split('&')
            out = dict()
            for q in queries:
                try:
                    k, v = re.match('^([^=]+)=(.*)$',q).groups()
                    out[k]=v
                except Exception as e:
                    Logger.log.error(f'Error processing WSGI query parameter {q} : {e}')
            return out
        except Exception as e:
            Logger.log.error(f'Error getting WSGI query parameters : {e}')
            return dict()

class WSGIApp:

    @classmethod
    def asCSV(cls,info):
        lines = []
        lines.append('timestamp,voltage,current,percentage')
        for row in info:
            row_str = [str(i) for i in row]
            lines.append(f"'{row_str[0]}',{row_str[1]},{row_str[2]},{row_str[3]}")
        return '\n'.join(lines)

    def __init__(self, json):
        self.json = json
        self.length = len(json)
        self.datastore = DataStore()

    def _responder(self, env):
        try:
            if env.method() == HTTPMethod.GET:
                return self.GET(env)
            else:
                return ErrorObject(status=HTTPStatus.BAD_REQUEST)
        except Exception as e:
            return ErrorObject(status=HTTPStatus.INTERNAL_SERVER_ERROR, text=str(e))

    def __call__(self, environ, start_response):
        env = WSGIEnv(environ)
        responder = self._responder(env)
        responder(start_response)
        return responder.text

    def GET(self,env):
        try:
            path = env.path()
            if len(path) == 0:
                pass
            elif path == 'cams':
                return DataObject(self.json)
            elif path == 'batt':
                params = env.query()
                if 'since' in params:
                    info = self.datastore.all_battery(params['since'])
                    return ResponseObject(content_type='text/csv',text=self.asCSV(info))
                else:
                    info = self.datastore.battery_json()
                    return DataObject(info)
            else:
                return ErrorObject(status=HTTPStatus.NOT_FOUND,
                                      text='NotFound')
        except Exception as e:
            Logger.log.error(f'Error: {e}')
            return ErrorObject(status=HTTPStatus.INTERNAL_SERVER_ERROR,
                                  text=str(e))








