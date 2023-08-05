from pydantic import BaseModel


class Record:
    _reserved_names = ("id",)

    def __init__(self, id: str):
        self.id = id
        self._data: dict[str, BaseModel] = {}

    def __getitem__(self, name: str) -> str | BaseModel:
        if name == "id":
            return self.id
        return self._data[name]

    def __setitem__(self, name: str, value: BaseModel) -> None:
        if name not in self._data and name not in self._reserved_names:
            self._data[name] = value
        else:
            raise AttributeError(f"DataObject attribute {name} already exists")
