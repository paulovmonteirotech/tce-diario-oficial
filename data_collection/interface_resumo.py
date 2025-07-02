import os
from tkinter import Tk, filedialog, messagebox

from llama_cpp import Llama
from PyPDF2 import PdfReader

# Caminho do modelo GGUF (ajuste se necessário)
MODEL_PATH = os.path.expanduser("~/modelos-llm/mistral.gguf")
llm = Llama(model_path=MODEL_PATH, n_ctx=4096)


def extrair_texto_pdf(caminho_pdf):
    leitor = PdfReader(caminho_pdf)
    texto = ""
    for pagina in leitor.pages:
        texto += pagina.extract_text() or ""
    return texto.strip()


def gerar_resumo(texto):
    # Limita o texto para não ultrapassar o contexto da IA
    contexto = texto[:3000]

    prompt = f"""
Você é um assistente que resume documentos oficiais.

Resumo do conteúdo abaixo:
\"\"\"
{contexto}
\"\"\"

Resumo:
"""
    resposta = llm(prompt, max_tokens=512, stop=["\nResumo"], echo=False)
    return resposta["choices"][0]["text"].strip()


def escolher_pdf_e_resumir():
    Tk().withdraw()
    caminho_pdf = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if not caminho_pdf:
        return

    texto = extrair_texto_pdf(caminho_pdf)
    if not texto:
        messagebox.showerror("Erro", "Não foi possível extrair texto do PDF.")
        return

    print("[📄] Gerando resumo com IA local...")
    resumo = gerar_resumo(texto)

    nome_base = os.path.splitext(os.path.basename(caminho_pdf))[0]
    arquivo_resumo = f"{nome_base}_resumo.txt"

    with open(arquivo_resumo, "w", encoding="utf-8") as f:
        f.write(resumo)

    print(f"[✔] Resumo salvo em: {arquivo_resumo}")
    messagebox.showinfo("Resumo gerado", resumo)


if __name__ == "__main__":
    escolher_pdf_e_resumir()
