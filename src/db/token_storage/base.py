from abc import (
    ABC,
    abstractmethod,
)
from typing import Any


class BaseTokenStorage(ABC):
    @abstractmethod
    def get_value(self, key: str) -> Any:
        pass

    @abstractmethod
    def set_value(self, key: str, token_value: Any) -> None:
        pass
