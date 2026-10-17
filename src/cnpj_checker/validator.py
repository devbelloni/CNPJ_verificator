"""CNPJ validation (numeric and the alphanumeric format introduced in 2026).

The two check digits are computed with a weighted modulo-11 sum. For alphanumeric CNPJs each
character is converted to ``ord(char) - 48``, so digits keep their value and letters map to
17..42, which is the method published by the Receita Federal.
"""

from __future__ import annotations

import re

_FIRST_WEIGHTS = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
_SECOND_WEIGHTS = [6, *_FIRST_WEIGHTS]
_BODY = re.compile(r"^[0-9A-Z]{12}[0-9]{2}$")


class InvalidCNPJ(ValueError):
    """Raised when a string is not a valid CNPJ."""


def clean_cnpj(value: str) -> str:
    """Strip punctuation and spaces and upper-case the value."""
    return re.sub(r"[^0-9A-Za-z]", "", value or "").upper()


def _check_digit(chars: str, weights: list[int]) -> int:
    total = sum((ord(c) - 48) * w for c, w in zip(chars, weights, strict=True))
    remainder = total % 11
    return 0 if remainder < 2 else 11 - remainder


def is_valid_cnpj(value: str) -> bool:
    cnpj = clean_cnpj(value)
    if not _BODY.match(cnpj) or len(set(cnpj)) == 1:
        return False
    first = _check_digit(cnpj[:12], _FIRST_WEIGHTS)
    second = _check_digit(cnpj[:12] + str(first), _SECOND_WEIGHTS)
    return cnpj[12:] == f"{first}{second}"


def format_cnpj(value: str) -> str:
    """Return the CNPJ as ``XX.XXX.XXX/XXXX-XX``; raises :class:`InvalidCNPJ` if invalid."""
    cnpj = clean_cnpj(value)
    if not is_valid_cnpj(cnpj):
        raise InvalidCNPJ(f"Invalid CNPJ: {value!r}")
    return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
