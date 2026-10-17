"""Validate Brazilian CNPJ numbers and look companies up through BrasilAPI."""

from .client import ApiError, Company, CompanyNotFound, fetch_company
from .validator import InvalidCNPJ, clean_cnpj, format_cnpj, is_valid_cnpj

__version__ = "1.0.0"
__all__ = [
    "ApiError", "Company", "CompanyNotFound", "InvalidCNPJ",
    "clean_cnpj", "fetch_company", "format_cnpj", "is_valid_cnpj",
]
