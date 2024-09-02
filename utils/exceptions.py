from rest_framework.exceptions import APIException

class GenericException(APIException):

    def __init__(self, detail=None, code=400):
        super().__init__(detail, code)

    status_code = 400
    default_detail = 'Not Exists!'


class NotExists(APIException):

    def __init__(self, detail=None, code=404):
        super().__init__(detail, code)

    status_code = 404
    default_detail = 'Not Exists!'

class Unauthorized(APIException):

    def __init__(self, detail=None, code=401):
        super().__init__(detail, code)

    status_code = 401
    default_detail = 'Unauthorized!'

class Unprocessable(APIException):

    def __init__(self, detail=None, code=422):
        super().__init__(detail, code)

    status_code = 401
    default_detail = 'Unprocessable entity!'