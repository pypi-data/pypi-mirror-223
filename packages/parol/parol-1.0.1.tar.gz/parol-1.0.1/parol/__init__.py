import hashlib
import secrets
import string
from typing import NamedTuple

__version__ = "1.0.1"

PASSWORD_LENGTH = 5
PASSWORD_MIN_DIGITS_COUNT = 3
ALGORITHM = "sha512"
ENCODING = "utf-8"
SALT_NBYTES = 32


class Password(NamedTuple):
    password: str
    salt: str

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return "Password(password='***')"

    @property
    def encoding(self) -> str:
        return ENCODING

    @property
    def algorithm(self) -> str:
        return ALGORITHM

    @property
    def hash(self) -> str:  # noqa:A003
        return hashlib.pbkdf2_hmac(
            self.algorithm,
            self.password.encode(self.encoding),
            self.salt.encode(self.encoding),
            100000,
        ).hex()

    @classmethod
    def generate(cls, length: int = PASSWORD_LENGTH) -> "Password":
        if length < PASSWORD_LENGTH:
            err = "Invalid password length"
            raise ValueError(err)

        alphabet = string.ascii_letters + string.digits

        while True:
            password = "".join(secrets.choice(alphabet) for _ in range(length))
            if all(
                (
                    any(c.islower() for c in password),
                    any(c.isupper() for c in password),
                    sum(c.isdigit() for c in password) >= PASSWORD_MIN_DIGITS_COUNT,
                ),
            ):
                break

        return cls(password=password, salt=secrets.token_hex(SALT_NBYTES))

    @staticmethod
    def validate(
        password: str,
        salt: str,
        hash: str,  # noqa:A002 pylint:disable=redefined-builtin
    ) -> bool:
        return Password(password=password, salt=salt).hash == hash

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Password):  # pragma:no cover
            return NotImplemented
        return self.password == other.password and self.salt == other.salt


def generate(length: int = PASSWORD_LENGTH) -> Password:
    return Password.generate(length=length)


def validate(
    password: str,
    salt: str,
    hash: str,  # noqa:A002 pylint:disable=redefined-builtin
) -> bool:
    return Password.validate(password, salt, hash)
