import logging
import traceback as tb
from collections.abc import Callable
from functools import wraps

__all__ = ("exception_decorator",)

logger = logging.getLogger(__name__)


def exception_decorator(func: Callable) -> Callable:
    """
    A decorator that wraps a function and handles exceptions.

    Args:
        func (Callable): The function to be decorated.

    Returns:
        Callable: A wrapped function that handles exceptions.
    """

    @wraps(func)
    def wrapper(*args: tuple, **kwargs: dict) -> None:
        try:
            logger.debug("Start")
            func(*args, **kwargs)
            logger.debug("Done!")
        except Exception as error:
            trace = tb.format_exception(
                type(error),
                error,
                error.__traceback__,
            )
            logger.error("\n".join(trace))

    return wrapper
