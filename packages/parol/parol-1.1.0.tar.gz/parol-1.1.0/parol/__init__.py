import secrets
import string
from typing import NamedTuple

import bcrypt

__version__ = "1.1.0"


class Password(NamedTuple):
    password: bytes

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return "Password(password='***')"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Password):  # pragma:no cover
            return NotImplemented
        return self.password == other.password

    def hash(self, rounds: int = 12) -> bytes:  # noqa:A003
        return bcrypt.hashpw(self.password, bcrypt.gensalt(rounds))

    def verify(
        self,
        hash: bytes,  # noqa:A002 pylint:disable=redefined-builtin
    ) -> bool:
        return bcrypt.checkpw(self.password, hash)

    @classmethod
    def gen(
        cls,
        length: int = 5,
        min_digits_count: int = 3,
        encoding: str = "utf-8",
    ) -> "Password":
        alphabet = string.ascii_letters + string.digits

        while True:
            password = "".join(secrets.choice(alphabet) for _ in range(length))
            if all(
                (
                    any(c.islower() for c in password),
                    any(c.isupper() for c in password),
                    sum(c.isdigit() for c in password) >= min_digits_count,
                ),
            ):
                break

        return cls(password.encode(encoding))
