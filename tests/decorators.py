from functools import wraps
from time import process_time
import loguru


def measure_time(func):
    @wraps(func)
    def time(*args, **kwargs):
        start = int(round(process_time() * 1000))
        try:
            return func(*args, **kwargs)
        finally:
            end_ = int(round(process_time() * 1000)) - start
            loguru.logger.info(f"Total execution time {func.__name__}: {end_ if end_ > 0 else 0} ms")
    return time
