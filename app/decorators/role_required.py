import sys
from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended.exceptions import NoAuthorizationError


class role_required(object):

    def __init__(self, roles):
        """
        If there are decorator arguments, the function
        to be decorated is not passed to the constructor!
        """
        self.__name__ = "role_required"
        self.roles = set(roles)

    def __call__(self, f):
        """
        If there are decorator arguments, __call__() is only called
        once, as part of the decoration process! You can only give
        it a single argument, which is the function object.
        """
        @wraps(f)
        def wrapped_func(*args, **kwargs):
            current_user = get_jwt_identity()
            if current_user:
                user_roles = current_user["roles"]
                for user_role in user_roles:
                    if user_role in self.roles:
                        return f(*args, **kwargs)
            raise NoAuthorizationError("Insufficient role")
        return wrapped_func
