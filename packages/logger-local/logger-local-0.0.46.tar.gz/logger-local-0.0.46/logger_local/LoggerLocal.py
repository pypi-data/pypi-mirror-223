from functools import wraps
from logger_local.LoggerService import LoggerService


logger_local = LoggerService()

def log_function_execution(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        object1 = {
            'args': str(args),
            'kawargs': str(kwargs),
        }
        logger_local.start(object=object1)
        result = func(*args, **kwargs)  # Execute the function
        object2 = {
            'result': result,
        }
        logger_local.end(object=object2)
        return result
    return wrapper