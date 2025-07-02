import subprocess
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk

# Lista de spiders disponíveis
SPIDERS = ["rj_macae", "sp_sao_paulo", "ba_salvador"]


def executar_spider():
    spider_name = combo_spider.get()
    start_date_str = entry_inicio.get()
    end_date_str = entry_fim.get()

    if not spider_name:
        messagebox.showerror("Erro", "Selecione uma cidade (spider).")
        return

    try:
        # Valida datas
        datetime.strptime(start_date_str, "%Y-%m-%d")
        datetime.strptime(end_date_str, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Erro", "Datas devem estar no formato YYYY-MM-DD.")
        return

    # Comando que simula o terminal: scrapy crawl spider -a start=... -a end=...
    comando = [
        "python",
        "-m",
        "scrapy",
        "crawl",
        spider_name,
        "-a",
        f"start={start_date_str}",
        "-a",
        f"end={end_date_str}",
    ]

    try:
        subprocess.run(comando, cwd="data_collection", check=True)
        messagebox.showinfo(
            "Sucesso", f"Spider '{spider_name}' executado com sucesso!\nPDFs baixados."
        )
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao executar o spider:\n\n{e}")


# Interface gráfica com tkinter
janela = tk.Tk()
janela.title("Interface - Querido Diário (com download de PDF)")
janela.geometry("400x250")
janela.resizable(False, False)

# Componentes da interface
tk.Label(janela, text="Selecione a cidade (spider):").pack(pady=5)
combo_spider = ttk.Combobox(janela, values=SPIDERS, state="readonly")
combo_spider.pack(pady=5)

tk.Label(janela, text="Data de início (YYYY-MM-DD):").pack()
entry_inicio = tk.Entry(janela)
entry_inicio.pack(pady=5)

tk.Label(janela, text="Data de fim (YYYY-MM-DD):").pack()
entry_fim = tk.Entry(janela)
entry_fim.pack(pady=5)

botao_executar = tk.Button(janela, text="Executar", command=executar_spider)
botao_executar.pack(pady=15)

janela.mainloop()
