class User:
    def __init__(self, id: int, name: str):
        self._id = id
        self._name = name

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @id.setter
    def set_id(self, id: int):
        self._id = id

    @name.setter
    def set_name(self, name: str):
        self._name = name
