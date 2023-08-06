from dataclasses import dataclass

from .identifier import Identifier


@dataclass(frozen=True)
class TableIdentifier(Identifier):  # pylint: disable=keyword-only-dataclass
    table_name: str

    @property
    def key(self) -> tuple[str]:
        return (self.table_name,)

    def __repr__(self) -> str:
        return f"""t["{self.table_name}"]"""
