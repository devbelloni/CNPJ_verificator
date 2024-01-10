import tkinter as tk
from tkinter import messagebox
import requests

def verificar_cnpj():
    cnpj = entry_cnpj.get().replace('.', '').replace('/', '')

    url_api = f'https://brasilapi.com.br/api/cnpj/v1/{cnpj}'

    try:
        response = requests.get(url_api)
        response.raise_for_status()

        dados_cnpj = response.json()

        nova_janela = tk.Toplevel(root)
        nova_janela.title('Dados da Empresa')

        tk.Label(nova_janela, text=f'Razão Social: {dados_cnpj.get("razao_social", "N/A")}').pack()
        tk.Label(nova_janela, text=f'Atividade Principal: {dados_cnpj.get("cnae_fiscal_descricao", "N/A")}').pack()
        tk.Label(nova_janela, text=f'Endereço: {dados_cnpj.get("logradouro", "N/A")} {dados_cnpj.get("numero", "N/A")} {dados_cnpj.get("bairro", "N/A")}').pack()
        tk.Label(nova_janela, text=f'Cidade: {dados_cnpj.get("municipio", "N/A")}').pack()
        tk.Label(nova_janela, text=f'UF: {dados_cnpj.get("uf", "N/A")}').pack()
        tk.Label(nova_janela, text=f'CEP: {dados_cnpj.get("cep", "N/A")}').pack()
        tk.Label(nova_janela, text=f'Telefone: {dados_cnpj.get("ddd_telefone_1", "N/A")}').pack()

    except requests.exceptions.RequestException as err:
        messagebox.showerror('Erro', f'Erro durante a requisição para o CNPJ {cnpj}. Erro: {err}')

root = tk.Tk()
root.title('Verificador de CNPJ')

tk.Label(root, text='CNPJ:').pack()
entry_cnpj = tk.Entry(root)
entry_cnpj.pack()

btn_enviar = tk.Button(root, text='Enviar', command=verificar_cnpj)
btn_enviar.pack()

root.mainloop()
