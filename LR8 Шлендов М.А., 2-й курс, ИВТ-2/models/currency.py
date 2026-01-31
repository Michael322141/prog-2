class Currency:
    def __init__(self, num_code: str, char_code: str, name: str, value: float, nominal: int, id: int | None = None):
        self._num_code = num_code
        self._char_code = char_code
        self._name = name
        self._value = value
        self._nominal = nominal
        self._id = id

    @property
    def id(self):
        return self._id

    @property
    def num_code(self):
        return self._num_code

    @property
    def char_code(self):
        return self._char_code

    @char_code.setter
    def char_code(self, val: str):
        if len(val) != 3:
            raise ValueError("Код валюты должен состоять из 3 символов")
        self._char_code = val.upper()

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val: float):
        if val < 0:
            raise ValueError("Курс валюты не может быть отрицательным")
        self._value = val

    @property
    def nominal(self):
        return self._nominal
    
    def __repr__(self) -> str:
        return f'{{"char_code": {self.char_code}, "name": {self.name}, "num_code": {self.num_code}, "value": {self.value}, "nominal": {self.nominal}}}'