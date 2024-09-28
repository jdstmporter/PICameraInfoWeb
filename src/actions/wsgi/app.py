from http import HTTPMethod

from .responses import BadRequestResponse, WSGIError, ServerErrorResponse, JSONResponse, Response, NotFoundResponse, \
    NotImplementedResponse, NoAuthorisationToken
from .environment import WSGIEnv
from data import DataStore


class WSGIAction:

    @classmethod
    def methods(cls):
        return []

    @classmethod
    def isSecure(cls):
        return False

    @classmethod
    def match(cls,env):
        return env.method() in cls.methods()




    def __init__(self,datastore,**kwargs):
        self.datastore=datastore
        self.env=WSGIEnv(dict())



    def authenticate(self):
        raise NoAuthorisationToken()

    def action(self):
        raise NotImplementedResponse()

    def __call__(self,env):
        self.env=env
        if self.isSecure():
            self.authenticate()
        return self.action()







class WSGIApp:

    @classmethod
    def asCSV(cls,info):
        lines = []
        lines.append('unix,timestamp,voltage,current,percentage')
        for row in info:
            row_str = [str(i) for i in row]
            lines.append(f"{row_str[0]},'{row_str[1]}',{row_str[2]},{row_str[3]},{row_str[4]}")
        return '\n'.join(lines)

    def __init__(self, json,api=None):
        self.json = json
        self.length = len(json)
        self.api=api
        self.datastore = DataStore()


    def actions(self, env):
        method = env.method()
        if method == HTTPMethod.GET:
            return self.GET(env)
        elif method == HTTPMethod.POST:
            return self.POST(env)
        elif method == HTTPMethod.DELETE:
            return self.DELETE(env)
        else:
            raise BadRequestResponse()

    def __call__(self, environ, start_response):
        try:
            env = WSGIEnv(environ)
            responder = self.actions(env)
            return responder(start_response)
        except WSGIError as w:
            return w(start_response)
        except Exception as e:
            return ServerErrorResponse(message=str(e))(start_response)


    def GET(self,env):
        path = env.path()
        if len(path) == 0:
            if self.api is None:
                return NotFoundResponse()
            else:
                return Response(text=self.api,content_type='application/yaml')
        elif path == 'cams':
            return JSONResponse(self.json)
        elif path == 'batt':
            params = env.query()
            if 'since' in params:
                info = self.datastore.all_battery_json(params['since'])
                #for row in info:
                #    ii = [str(type(r)) for r in row]
                #    print(', '.join(ii))
                return JSONResponse(info)
            else:
                info = self.datastore.battery_json()
                return JSONResponse(info)
        else:
            raise NotFoundResponse()

    def POST(self,env):
        auth = env.auth_key()
        raise NotImplementedResponse()

    def DELETE(self,env):
        auth = env.auth_key()
        raise NotImplementedResponse()










