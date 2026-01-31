class Author:
    def __init__(self, name: str, group: str):
        self._name = name
        self._group = group

    @property
    def name(self) -> str:
        return self._name

    @property
    def group(self) -> str:
        return self._group

    @group.setter
    def set_group(self, group: str):
        self._group = group
        
    @name.setter
    def set_name(self, name: str):
        self._name = name

