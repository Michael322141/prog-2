class UserCurrency:
    def __init__(self, user_id: int, currency_id: str, id: int = 0):
        self._id = id
        self._user_id = user_id
        self._currency_id = currency_id

    @property
    def id(self) -> int:
        return self._id

    @property
    def user_id(self) -> int:
        return self._user_id

    @property
    def currency_id(self) -> str:
        return self._currency_id

    @id.setter
    def set_id(self, id: int):
        self._id = id

    @user_id.setter
    def set_user_id(self, user_id: int):
        self._user_id = user_id

    @currency_id.setter
    def set_currency_id(self, currency_id: str):
        self._currency_id = currency_id
