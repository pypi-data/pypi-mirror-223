from typing import Any, Callable, Dict, List, overload, Tuple


class InvalidHandlerError(TypeError):

    def __init__(self, handler: object) -> None:
        name = type(handler).__name__
        message = f"Can't add non-callable '{name}' object as a handler!"
        super().__init__(message)


class Event:

    def __init__(self):
        self.__handlers: List[Callable] = []
        self.__returns: Dict[Callable, Any] = {}

    @overload
    def __and__(self, handler: Callable) -> Any:
        ...

    @overload
    def __and__(self, handlers: Tuple[Callable]) -> Dict[Callable, Any]:
        ...

    def __and__(self, other):
        if isinstance(other, tuple):
            return self.get_returns(other)
        else:
            return self.get_return(other)

    def __call__(self, *args, **kwargs):
        self.invoke(*args, **kwargs)

    def __iadd__(self, handler: Callable):
        self.add_handler(handler)
        return self

    def __isub__(self, handler: Callable):
        self.remove_handler(handler)
        return self

    @property
    def returns(self):
        return self.__returns

    def add_handler(self, handler: Callable) -> None:
        if not callable(handler):
            raise InvalidHandlerError(handler)
        if not self.has_handler(handler):
            self.__handlers.append(handler)

    def has_handler(self, handler: Callable) -> bool:
        return handler in self.__handlers

    def remove_handler(self, handler: Callable) -> None:
        if self.has_handler(handler):
            self.__handlers.remove(handler)

    def get_return(self, handler: Callable) -> Any:
        try:
            return self.returns[handler]
        except KeyError:
            return None

    def get_returns(self, handlers: Tuple[Callable]) -> Dict[Callable, Any]:
        returns = {}
        for handler in handlers:
            returns[handler] = self.get_return(handler)
        return returns

    def invoke(self, *args, **kwargs) -> None:
        self.__returns = {}
        for handler in self.__handlers:
            self.__returns[handler] = handler(*args, **kwargs)
