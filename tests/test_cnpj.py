import pytest
import requests

from cnpj_checker import (
    ApiError,
    CompanyNotFound,
    InvalidCNPJ,
    clean_cnpj,
    fetch_company,
    format_cnpj,
    is_valid_cnpj,
)
from cnpj_checker.__main__ import main

VALID = "11.222.333/0001-81"


@pytest.mark.parametrize("value", [VALID, "11222333000181", " 11.222.333/0001-81 ", "12.ABC.345/01DE-35"])
def test_valid_cnpjs(value):
    assert is_valid_cnpj(value)


@pytest.mark.parametrize(
    "value", ["", "123", "11111111111111", "11.222.333/0001-82", "12.ABC.345/01DE-36", "abc", None]
)
def test_invalid_cnpjs(value):
    assert not is_valid_cnpj(value)


def test_clean_and_format():
    assert clean_cnpj(" 11.222.333/0001-81 ") == "11222333000181"
    assert format_cnpj("11222333000181") == VALID
    with pytest.raises(InvalidCNPJ):
        format_cnpj("11222333000180")


class FakeResponse:
    def __init__(self, status, payload=None):
        self.status_code = status
        self._payload = payload or {}

    def json(self):
        return self._payload


class FakeSession:
    def __init__(self, response=None, error=None):
        self.response, self.error, self.calls = response, error, []

    def get(self, url, timeout):
        self.calls.append((url, timeout))
        if self.error:
            raise self.error
        return self.response


def test_fetch_company_success():
    payload = {"razao_social": "ACME LTDA", "uf": "SP", "municipio": "SAO PAULO", "numero": 10}
    session = FakeSession(FakeResponse(200, payload))
    company = fetch_company(VALID, session=session)
    assert company.legal_name == "ACME LTDA" and company.number == "10"
    assert company.phone == "N/A"
    assert session.calls[0][0].endswith("/11222333000181")


def test_invalid_cnpj_makes_no_request():
    session = FakeSession(FakeResponse(200))
    with pytest.raises(InvalidCNPJ):
        fetch_company("123", session=session)
    assert session.calls == []


def test_not_found_and_http_errors():
    with pytest.raises(CompanyNotFound):
        fetch_company(VALID, session=FakeSession(FakeResponse(404)))
    with pytest.raises(ApiError, match="500"):
        fetch_company(VALID, session=FakeSession(FakeResponse(500)))


def test_network_failure_becomes_api_error():
    with pytest.raises(ApiError):
        fetch_company(VALID, session=FakeSession(error=requests.ConnectionError("down")))


def test_cli_rejects_invalid_input(capsys):
    assert main(["123"]) == 1
    assert "Invalid CNPJ" in capsys.readouterr().err
