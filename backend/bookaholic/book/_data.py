from typing import Any, Dict, Self


class Data(dict):
    _Data = Dict[str, Any]

    @classmethod
    def from_data(cls, data: _Data) -> Self:
        return cls(**data)

    def to_data(self) -> _Data:
        return self.copy()