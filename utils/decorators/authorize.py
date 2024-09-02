from utils.jwt_builder import JwtBuilder
from utils.exceptions import Unauthorized

def is_authorize(role:list=None):
    def inner(func):
        def wrapper(*args, **kwargs):
            request=args[1]
            if request.META.get('HTTP_AUTHORIZATION'):
                token=request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
                token_data=JwtBuilder(token=token).decode()
                if token_data:
                    if role and token_data.get('role') not in role:
                        message=",".join(role)
                        raise Unauthorized(detail=f"can only be accessed by {message}")
                    args[1].token_data=token_data
                    return func(*args,**kwargs)
                
            raise Unauthorized()

        return wrapper
    
    return inner