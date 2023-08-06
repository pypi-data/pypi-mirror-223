from abc import ABC, abstractmethod
from typing import Any

_ = Any


class ABCNetworkClient(ABC):
    @abstractmethod
    def construct_form(self, data: dict) -> _:
        pass

    @abstractmethod
    async def request_text(
        self, url: str, method: str = "get", data: dict | None = None, **kw
    ) -> str:
        pass

    @abstractmethod
    async def request_json(
        self, url: str, method: str = "get", data: dict | None = None, **kw
    ) -> dict:
        pass

    @abstractmethod
    async def request_bytes(
        self, url: str, method: str = "get", data: dict | None = None, **kw
    ) -> bytes:
        pass

    @abstractmethod
    async def close(self) -> None:
        pass

    async def __aenter__(self) -> "ABCNetworkClient":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()
