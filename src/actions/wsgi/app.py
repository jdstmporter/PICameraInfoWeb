from http import HTTPMethod

from .responses import BadRequestResponse, WSGIError, ServerErrorResponse, JSONResponse, Response, NotFoundResponse
from .environment import WSGIEnv
from data import DataStore







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


    def actions(self, env):
        if env.method() == HTTPMethod.GET:
            return self.GET(env)
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
            return Response(text='Should be OpenAPI spec')
        elif path == 'cams':
            return JSONResponse(self.json)
        elif path == 'batt':
            params = env.query()
            if 'since' in params:
                info = self.datastore.all_battery(params['since'])
                return Response(content_type='text/csv',text=self.asCSV(info))
            else:
                info = self.datastore.battery_json()
                return JSONResponse(info)
        else:
            raise NotFoundResponse()








