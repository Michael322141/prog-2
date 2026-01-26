class Currency:
    def __init__(self, id: str, num_code: int, char_code: str, name: str, value: float, nominal: int):
        self._id = id
        self._num_code = num_code
        self._char_code = char_code
        self._name = name
        self._value = value
        self._nominal = nominal

    @property
    def id(self) -> str:
        return self._id

    @property
    def num_code(self) -> int:
        return self._num_code

    @property
    def char_code(self) -> str:
        return self._char_code

    @property
    def name(self) -> str:
        return self._name

    @property
    def value(self) -> float:
        return self._value

    @property
    def nominal(self) -> int:
        return self._nominal

    @id.setter
    def set_id(self, id: str):
        self._id = id

    @num_code.setter
    def set_num_code(self, num_code: int):
        self._num_code = num_code

    @char_code.setter
    def set_char_code(self, char_code: str):
        self._char_code = char_code

    @name.setter
    def set_name(self, name: str):
        self._name = name

    @value.setter
    def set_value(self, value: float):
        self._value = value

    @nominal.setter
    def set_nominal(self, nominal: int):
        self._nominal = nominal
