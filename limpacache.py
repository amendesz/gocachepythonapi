import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import requests

def clear_cache():
    url = entry_url.get()
    headers = {
        'GoCache-Token': 'SEU_TOKEN_AQUI'
    }

    response = requests.delete(url, headers=headers)

    if response.status_code == 200:
        messagebox.showinfo('Sucesso', 'Cache do domínio limpo com sucesso!')
    else:
        messagebox.showerror('Erro', f'Erro ao limpar o cache: {response.status_code}')

def query_domain():
    domain = entry_domain.get()

    url = f'{base_url}/dns/{domain}'
    headers = {
        'GoCache-Token': 'SEU_TOKEN_AQUI'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if "response" in data and "records" in data["response"]:
            records = data["response"]["records"]
            result_text.delete('1.0', tk.END)
            result_text_tags.config(state=tk.NORMAL)
            result_text_tags.delete('1.0', tk.END)
            for record in records:
                name = record["name"]
                content = record["content"]

                friendly_name = name.replace('.SEU_DOMINIO_AQUI', '')
                friendly_content = content.replace(';', '\n')

                result_text.insert(tk.END, f"Name: {friendly_name}\n")
                result_text.insert(tk.END, f"Content:\n{friendly_content}\n")
                result_text.insert(tk.END, "\n")

                result_text_tags.insert(tk.END, f"{friendly_name}\n")
                result_text_tags.insert(tk.END, f"{friendly_content}\n")

            result_text_tags.config(state=tk.DISABLED)
        else:
            result_text.delete('1.0', tk.END)
            result_text.insert(tk.END, "Resposta inválida do servidor.")
    else:
        result_text.delete('1.0', tk.END)
        result_text.insert(tk.END, f"Erro na requisição: {response.status_code}")

def search_text():
    keyword = entry_search.get().lower()
    content = result_text_tags.get('1.0', tk.END).lower()

    result_text_tags.tag_remove('highlight', '1.0', tk.END)
    count = 0
    idx = '1.0'
    while idx:
        idx = result_text_tags.search(keyword, idx, nocase=True, stopindex=tk.END)
        if idx:
            count += 1
            end_idx = f"{idx}+{len(keyword)}c"
            result_text_tags.tag_add('highlight', idx, end_idx)
            idx = end_idx

    if count > 0:
        messagebox.showinfo('Resultado da busca', f'A palavra "{keyword}" foi encontrada {count} vezes.')
        result_text.see(result_text_tags.index(f"{idx}-1c"))
        result_text_tags.see(idx)
    else:
        messagebox.showinfo('Resultado da busca', f'A palavra "{keyword}" não foi encontrada.')

def update_search_results(*args):
    keyword = entry_search.get().lower()
    content = result_text_tags.get('1.0', tk.END).lower()

    result_text_tags.tag_remove('highlight', '1.0', tk.END)
    count = 0
    idx = '1.0'
    while idx:
        idx = result_text_tags.search(keyword, idx, nocase=True, stopindex=tk.END)
        if idx:
            count += 1
            end_idx = f"{idx}+{len(keyword)}c"
            result_text_tags.tag_add('highlight', idx, end_idx)
            idx = end_idx

    if count > 0:
        result_text.see(result_text_tags.index(f"{idx}-1c"))
        result_text_tags.see(idx)

base_url = 'https://api.gocache.com.br/v1'

window = tk.Tk()
window.title('GoCache API')
window.geometry('600x400')

tab_control = ttk.Notebook(window)

query_tab = tk.Frame(tab_control)
tab_control.add(query_tab, text='Consulta de Domínios')

domain_label = tk.Label(query_tab, text='Domínio:')
domain_label.pack()
entry_domain = tk.Entry(query_tab, width=40)
entry_domain.pack()

query_button = tk.Button(query_tab, text='Consultar', command=query_domain)
query_button.pack()

result_frame = ttk.Frame(query_tab)
result_frame.pack(fill='both', expand=True)

scrollbar = tk.Scrollbar(result_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

result_text = tk.Text(result_frame, height=10, width=60, yscrollcommand=scrollbar.set)
result_text.pack(side=tk.LEFT, fill='both', expand=True)

scrollbar.config(command=result_text.yview)

search_frame = ttk.Frame(query_tab)
search_frame.pack(fill='both', expand=True)

search_label = tk.Label(search_frame, text='Palavra a ser buscada:')
search_label.pack()
entry_search = tk.Entry(search_frame, width=40)
entry_search.pack()

result_text_tags = tk.Text(search_frame, height=5, width=60, yscrollcommand=scrollbar.set)
result_text_tags.pack(side=tk.LEFT, fill='both', expand=True)
result_text_tags.config(state=tk.DISABLED)

entry_search.bind('<KeyRelease>', update_search_results)

search_button = tk.Button(search_frame, text='Buscar', command=search_text)
search_button.pack()

cache_tab = tk.Frame(tab_control)
tab_control.add(cache_tab, text='Limpeza de Cache')

url_label = tk.Label(cache_tab, text='URL do Domínio:')
url_label.pack()
entry_url = tk.Entry(cache_tab, width=40)
entry_url.pack()

clear_button = tk.Button(cache_tab, text='Limpar Cache', command=clear_cache)
clear_button.pack()

tab_control.pack(expand=True, fill='both')

window.mainloop()
