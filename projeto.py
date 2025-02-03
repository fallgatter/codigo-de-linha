import tkinter as tk
from tkinter import messagebox
import socket
import threading
import matplotlib.pyplot as plt
import numpy as np

# Configurações de rede
HOST = '127.0.0.1'  # Localhost (substitua pelo IP do servidor)
PORT = 65432        # Porta de comunicação

# Função para codificação AMI
def ami_encode(binary_str):
    ami_signal = []
    last_polarity = 1  # Começa com polaridade positiva
    for bit in binary_str:
        if bit == '1':
            ami_signal.append(last_polarity)
            last_polarity *= -1  # Alterna a polaridade
        else:
            ami_signal.append(0)
    return ami_signal

# Função para decodificação AMI
def ami_decode(ami_signal):
    binary_str = ''
    for value in ami_signal:
        if value != 0:
            binary_str += '1'
        else:
            binary_str += '0'
    return binary_str

# Função para criptografar (Cifra de César)
def encrypt(text, shift=3):
    encrypted_text = ''
    for char in text:
        if char.isalpha():
            shift_amount = shift % 26
            if char.islower():
                encrypted_text += chr(((ord(char) - ord('a') + shift_amount) % 26) + ord('a'))
            else:
                encrypted_text += chr(((ord(char) - ord('A') + shift_amount) % 26) + ord('A'))
        else:
            encrypted_text += char
    return encrypted_text

# Função para descriptografar (Cifra de César)
def decrypt(text, shift=3):
    return encrypt(text, -shift)

# Função para converter texto em binário (ASCII estendido)
def text_to_binary(text):
    binary_str = ''
    for char in text:
        binary_str += format(ord(char), '08b')  # Converte cada caractere para 8 bits
    return binary_str

# Função para converter binário em texto (ASCII estendido)
def binary_to_text(binary_str):
    text = ''
    for i in range(0, len(binary_str), 8):
        byte = binary_str[i:i+8]
        text += chr(int(byte, 2))
    return text

# Função para gerar o gráfico da forma de onda
def plot_waveform(signal, title):
    plt.figure()
    plt.step(range(len(signal)), signal, where='post')
    plt.title(title)
    plt.xlabel('Bit')
    plt.ylabel('Amplitude')
    plt.grid(True)
    plt.show()

# Função para enviar mensagem
def send_message():
    text = entry.get()
    if not text:
        messagebox.showerror("Erro", "Digite uma mensagem!")
        return

    # Criptografa a mensagem
    encrypted_text = encrypt(text)
    # Converte para binário
    binary_str = text_to_binary(encrypted_text)
    # Codifica em AMI
    ami_signal = ami_encode(binary_str)

    # Mostra os dados na interface
    msg_original.config(text=f"Mensagem Original: {text}")
    msg_cripto.config(text=f"Mensagem Criptografada: {encrypted_text}")
    msg_binario.config(text=f"Mensagem em Binário: {binary_str}")
    msg_ami.config(text=f"Mensagem Codificada (AMI): {ami_signal}")

    # Gera o gráfico da forma de onda
    plot_waveform(ami_signal, "Forma de Onda AMI (Envio)")

    # Envia a mensagem codificada via rede
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(str(ami_signal).encode())
    except Exception as e:
        messagebox.showerror("Erro", f"Falha na comunicação: {e}")

# Função para receber mensagem
def receive_message():
    def listen():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            conn, addr = s.accept()
            with conn:
                data = conn.recv(1024).decode()
                ami_signal = eval(data)  # Converte a string de volta para lista

                # Decodifica o AMI para binário
                binary_str = ami_decode(ami_signal)
                # Converte binário para texto
                encrypted_text = binary_to_text(binary_str)
                # Descriptografa a mensagem
                text = decrypt(encrypted_text)

                # Mostra os dados na interface
                msg_recebida.config(text=f"Mensagem Recebida: {text}")
                msg_binario_recebido.config(text=f"Mensagem em Binário: {binary_str}")
                msg_ami_recebido.config(text=f"Mensagem Codificada (AMI): {ami_signal}")

                # Gera o gráfico da forma de onda
                plot_waveform(ami_signal, "Forma de Onda AMI (Recepção)")

    # Inicia a escuta em uma thread separada
    threading.Thread(target=listen).start()

# Interface gráfica
root = tk.Tk()
root.title("Codificação AMI")

# Entrada de texto
tk.Label(root, text="Digite a mensagem:").pack()
entry = tk.Entry(root, width=50)
entry.pack()

# Botões
tk.Button(root, text="Enviar Mensagem", command=send_message).pack()
tk.Button(root, text="Receber Mensagem", command=receive_message).pack()

# Labels para exibir informações
msg_original = tk.Label(root, text="Mensagem Original:")
msg_original.pack()
msg_cripto = tk.Label(root, text="Mensagem Criptografada:")
msg_cripto.pack()
msg_binario = tk.Label(root, text="Mensagem em Binário:")
msg_binario.pack()
msg_ami = tk.Label(root, text="Mensagem Codificada (AMI):")
msg_ami.pack()

msg_recebida = tk.Label(root, text="Mensagem Recebida:")
msg_recebida.pack()
msg_binario_recebido = tk.Label(root, text="Mensagem em Binário:")
msg_binario_recebido.pack()
msg_ami_recebido = tk.Label(root, text="Mensagem Codificada (AMI):")
msg_ami_recebido.pack()

root.mainloop()