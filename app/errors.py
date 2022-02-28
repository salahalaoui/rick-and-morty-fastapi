from typing import List


class CrudError(Exception):
    pass


class ElementNotFound(CrudError):
    pass


class ElementAlreadyExistsError(CrudError):
    pass


class CharactersAlreadyExistError(CrudError):
    pass
