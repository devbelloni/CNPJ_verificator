"""``python -m cnpj_checker``: GUI without arguments, command line with a CNPJ."""

from __future__ import annotations

import sys

from .client import ApiError, CompanyNotFound, fetch_company
from .validator import InvalidCNPJ, format_cnpj


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if not args:
        from .gui import main as gui_main

        gui_main()
        return 0
    try:
        company = fetch_company(args[0])
    except (InvalidCNPJ, CompanyNotFound, ApiError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(f"{format_cnpj(company.cnpj)}  {company.legal_name}")
    print(f"{company.main_activity} | {company.status} | {company.city}/{company.state}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
