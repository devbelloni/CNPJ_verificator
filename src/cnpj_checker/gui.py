"""Tkinter desktop front end."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from .client import ApiError, CompanyNotFound, fetch_company
from .validator import InvalidCNPJ, format_cnpj


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("CNPJ Verificator")
        self.resizable(False, False)
        frame = ttk.Frame(self, padding=16)
        frame.grid()
        ttk.Label(frame, text="CNPJ:").grid(row=0, column=0, sticky="w")
        self.entry = ttk.Entry(frame, width=26)
        self.entry.grid(row=0, column=1, padx=8)
        self.entry.bind("<Return>", lambda _e: self.lookup())
        ttk.Button(frame, text="Check", command=self.lookup).grid(row=0, column=2)
        self.result = tk.StringVar()
        ttk.Label(frame, textvariable=self.result, justify="left").grid(
            row=1, column=0, columnspan=3, sticky="w", pady=(12, 0)
        )

    def lookup(self) -> None:
        try:
            company = fetch_company(self.entry.get())
        except InvalidCNPJ:
            messagebox.showwarning("Invalid CNPJ", "The number is not a valid CNPJ.")
        except CompanyNotFound:
            messagebox.showinfo("Not found", "No company is registered with this CNPJ.")
        except ApiError as exc:
            messagebox.showerror("Service error", str(exc))
        else:
            self.result.set(
                f"{format_cnpj(company.cnpj)}\n{company.legal_name}\n"
                f"Activity: {company.main_activity}\nStatus: {company.status}\n"
                f"Address: {company.street}, {company.number} - {company.district}\n"
                f"{company.city}/{company.state}  CEP {company.zip_code}\nPhone: {company.phone}"
            )


def main() -> None:
    App().mainloop()
