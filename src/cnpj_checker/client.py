"""BrasilAPI client."""

from __future__ import annotations

from dataclasses import dataclass

import requests

from .validator import InvalidCNPJ, clean_cnpj, is_valid_cnpj

BASE_URL = "https://brasilapi.com.br/api/cnpj/v1"


class ApiError(RuntimeError):
    """The service failed or answered with an unexpected status."""


class CompanyNotFound(LookupError):
    """The CNPJ is valid but not registered."""


@dataclass(frozen=True)
class Company:
    cnpj: str
    legal_name: str
    trade_name: str
    main_activity: str
    status: str
    street: str
    number: str
    district: str
    city: str
    state: str
    zip_code: str
    phone: str

    @classmethod
    def from_api(cls, cnpj: str, data: dict) -> Company:
        def get(key: str) -> str:
            value = data.get(key)
            return str(value).strip() if value not in (None, "") else "N/A"

        return cls(
            cnpj=cnpj,
            legal_name=get("razao_social"),
            trade_name=get("nome_fantasia"),
            main_activity=get("cnae_fiscal_descricao"),
            status=get("descricao_situacao_cadastral"),
            street=get("logradouro"),
            number=get("numero"),
            district=get("bairro"),
            city=get("municipio"),
            state=get("uf"),
            zip_code=get("cep"),
            phone=get("ddd_telefone_1"),
        )


def fetch_company(
    cnpj: str, session: requests.Session | None = None, timeout: float = 10.0
) -> Company:
    """Look up a company. Validates the CNPJ locally first, so bad input costs no request."""
    digits = clean_cnpj(cnpj)
    if not is_valid_cnpj(digits):
        raise InvalidCNPJ(f"Invalid CNPJ: {cnpj!r}")
    http = session or requests
    try:
        response = http.get(f"{BASE_URL}/{digits}", timeout=timeout)
    except requests.RequestException as exc:
        raise ApiError(f"Could not reach BrasilAPI: {exc}") from exc
    if response.status_code in (400, 404):
        raise CompanyNotFound(f"No company found for CNPJ {digits}")
    if response.status_code != 200:
        raise ApiError(f"BrasilAPI returned HTTP {response.status_code}")
    return Company.from_api(digits, response.json())
