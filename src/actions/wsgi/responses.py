
from http import HTTPStatus

class Response:

    def __init__(self, status=HTTPStatus.OK, content_type='text/plain', text=''):
        self.status = f'{status.value} {status.phrase}'
        self.headers = [('Content-type', content_type)]
        self.text = [text.encode('utf-8')]

    def __call__(self,respond):
        respond(self.status, self.headers)
        return self.text



class JSONResponse(Response):
    def __init__(self,json):
        super().__init__(content_type='application/json',text=json)


class WSGIError(Exception):
    def __init__(self,status,message=''):
        super().__init__()
        self.response = Response(status=status, text=message)

    def __call__(self,respond):
        self.response(respond)
        return self.response.text


class NotFoundResponse(WSGIError):
    def __init__(self,message=''):
        super().__init__(status=HTTPStatus.NOT_FOUND,message=message)

class ServerErrorResponse(WSGIError):
    def __init__(self,message=''):
        super().__init__(status=HTTPStatus.INTERNAL_SERVER_ERROR,message=message)

class BadRequestResponse(WSGIError):
    def __init__(self, message=''):
        super().__init__(status=HTTPStatus.BAD_REQUEST, message=message)

class UnauthorisedResponse(WSGIError):
    def __init__(self,message=''):
        super().__init__(status=HTTPStatus.UNAUTHORIZED, message=message)

