import time
from functools import wraps


def singleton(cls):
    """Декоратор синглтона"""

    @wraps(cls)
    def wrapper(*args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = cls(*args, **kwargs)
        return cls._instance

    return wrapper


def time_sleep_after(seconds: int):
    """
    Декоратор для ожидания времени после выполнения функции.
    Функция НЕ должна возвращать результат.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
            finally:
                time.sleep(seconds)

        return wrapper

    return decorator
