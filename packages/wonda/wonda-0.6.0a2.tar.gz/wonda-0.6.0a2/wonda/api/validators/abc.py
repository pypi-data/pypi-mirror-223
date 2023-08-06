from abc import ABC, abstractmethod
from typing import Any


class ABCRequestValidator(ABC):
    @abstractmethod
    async def validate(self, data: dict) -> Any:
        pass


class ABCResponseValidator(ABC):
    @abstractmethod
    async def validate(self, response: bytes) -> bytes:
        pass
