#Programa para baixar músicas do YouTube em MP3
#Usa a biblioteca yt-dlp para baixar o áudio ($ pip install yt-dlp)
#Usa a biblioteca tkinter para criar a interface gráfica ($ pip install tk)
#Usa a biblioteca ffmpeg para converter o áudio para MP3, não esquecer de adiconar ao path do sistema

import os
import yt_dlp
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

def baixar_audio(link, log_area, destino):
    if not destino:
        messagebox.showwarning("Destino não selecionado", "Por favor, selecione uma pasta de destino.")
        return

    if not os.path.exists(destino):
        os.makedirs(destino)

    opcoes = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(destino, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'noplaylist': True,
        'progress_hooks': [lambda d: atualizar_log(d, log_area)]
    }

    with yt_dlp.YoutubeDL(opcoes) as ydl:
        try:
            ydl.download([link])
        except Exception as e:
            log_area.insert(tk.END, f"❌ Erro: {e}\n")
            log_area.see(tk.END)

def atualizar_log(d, log_area):
    if d['status'] == 'finished':
        log_area.insert(tk.END, f"✅ Baixado: {d['filename']}\n")
        log_area.see(tk.END)

def baixar_link_manual(entry_link, log_area, destino):
    link = entry_link.get().strip()
    if not destino:
        messagebox.showwarning("Destino não selecionado", "Por favor, selecione uma pasta de destino.")
        return
    if link.startswith('http'):
        log_area.insert(tk.END, f"🔗 Iniciando download: {link}\n")
        baixar_audio(link, log_area, destino)
    else:
        messagebox.showwarning("Link inválido", "Digite um link válido do YouTube.")

def baixar_links_do_arquivo(log_area, destino):
    if not destino:
        messagebox.showwarning("Destino não selecionado", "Por favor, selecione uma pasta de destino.")
        return

    caminho_arquivo = filedialog.askopenfilename(
        title="Selecione o arquivo .txt com os links",
        filetypes=[("Arquivos de Texto", "*.txt")]
    )
    if not caminho_arquivo:
        return

    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        links = [linha.strip() for linha in f if linha.strip()]

    for link in links:
        log_area.insert(tk.END, f"🔗 Baixando: {link}\n")
        baixar_audio(link, log_area, destino)

def escolher_diretorio(entry_destino):
    pasta = filedialog.askdirectory()
    if pasta:
        entry_destino.config(state="normal")
        entry_destino.delete(0, tk.END)
        entry_destino.insert(0, pasta)
        entry_destino.config(state="readonly")

def iniciar_interface():
    root = tk.Tk()
    root.title("YouTube MP3 Downloader")
    root.geometry("650x450")
    root.resizable(False, False)

    # Label do link
    label = tk.Label(root, text="Cole o link do YouTube abaixo:", font=("Arial", 12))
    label.pack(pady=10)

    # Campo do link
    entry_link = tk.Entry(root, width=70)
    entry_link.pack(pady=5)

    # Seletor de diretório
    frame_destino = tk.Frame(root)
    frame_destino.pack(pady=5)

    entry_destino = tk.Entry(frame_destino, width=55, state="readonly")
    entry_destino.grid(row=0, column=0, padx=5)

    btn_escolher_pasta = tk.Button(frame_destino, text="Selecionar pasta", command=lambda: escolher_diretorio(entry_destino))
    btn_escolher_pasta.grid(row=0, column=1, padx=5)

    # Botões principais
    frame_botoes = tk.Frame(root)
    frame_botoes.pack(pady=10)

    btn_baixar = tk.Button(frame_botoes, text="Baixar Link", width=15,
                           command=lambda: baixar_link_manual(entry_link, log_area, entry_destino.get()))
    btn_baixar.grid(row=0, column=0, padx=10)

    btn_arquivo = tk.Button(frame_botoes, text="Baixar de Arquivo .txt", width=20,
                            command=lambda: baixar_links_do_arquivo(log_area, entry_destino.get()))
    btn_arquivo.grid(row=0, column=1, padx=10)

    btn_sair = tk.Button(frame_botoes, text="Sair", width=10, command=root.quit)
    btn_sair.grid(row=0, column=2, padx=10)

    # Área de log
    log_area = scrolledtext.ScrolledText(root, width=80, height=12)
    log_area.pack(pady=10)
    log_area.insert(tk.END, "💡 Selecione a pasta de destino antes de começar.\n")

    root.mainloop()

if __name__ == "__main__":
    iniciar_interface()
