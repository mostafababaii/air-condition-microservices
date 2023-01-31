from functools import wraps


def catch_endpoint_exeptions(*exceptions, default_status_code=500, default_exception=None):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except exceptions as e:
                if callable(default_exception):
                    return default_exception()
                return {"error": str(e)}, default_status_code
        return wrapper
    return decorator
