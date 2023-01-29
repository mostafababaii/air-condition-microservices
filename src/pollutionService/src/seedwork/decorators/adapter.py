from rest_framework.serializers import Serializer
from rest_framework.response import Response
from rest_framework import status
from typing import Callable, List, Dict


def serialize(serializer: Serializer) -> Callable:
    def func(f: Callable) -> Callable:
        def wrapper(*args: tuple, **kwargs: Dict):
            s = serializer(data=args[0].data)
            if not s.is_valid():
                return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)
            return f(*args, **kwargs)

        return wrapper

    return func


def exception_handler(exceptions: List[Exception]) -> Callable:
    def func(f: Callable) -> Callable:
        def wrapper(*args: tuple, **kwargs: Dict):
            try:
                return f(*args, **kwargs)
            except Exception as e:
                if type(e) in exceptions:
                    return Response(
                        data={"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST
                    )
                raise e

        return wrapper

    return func
