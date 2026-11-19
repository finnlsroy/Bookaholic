from typing import Any, Dict, Self

from datetime import date


class Data(dict):
    _Data = Dict[str, Any]

    @classmethod
    def from_data(cls, data: _Data) -> Self:
        return cls(**data)

    def to_data(self) -> _Data:
        data = {}

        for key, val in self.items():
            
            if type(val) is date:
                data[key] = val.strftime("%Y-%m-%d")
            else:
                data[key] = val
        
        return data