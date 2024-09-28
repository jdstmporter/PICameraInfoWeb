import re
from http import HTTPMethod

from actions.wsgi.responses import NoAuthorisationToken
from util import Logger

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

    def auth_key(self):
        try:
            return self._env['HTTP_AUTHORIZATION']
        except Exception as e:
            Logger.log.error(f'Cannot get authorization token : {e}')
            raise NoAuthorisationToken()


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