from abc import ABC, abstractmethod


class Identifier(ABC):
    @abstractmethod
    def __repr__(self) -> str:
        ...

    def __str__(self) -> str:
        return repr(self)
