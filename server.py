from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import matplotlib.pyplot as plt
import socket
import threading
import tkinter as tk

def xor_cipher(texto, chave):
    resultado = ""
    for i, char in enumerate(texto):
        resultado += chr(ord(char) ^ ord(chave[i % len(chave)]))
    return resultado

def recarregar():
    refresh.set(True)

def toggle_server():
    if server_var.get():
        if not thread.is_alive():
            thread.start()
            print("Servidor iniciado!")
    else:
        print("Servidor parado")

def texto_para_binario(texto):
    binario = ''
    for char in texto:
        binario += '{:08b}'.format(ord(char))
    return binario

def binario_para_texto(binario):
    texto = ''
    for bit in range(0, len(binario), 8):
        texto += chr(int(binario[bit:bit+8], 2))
    return texto

def AMI(binario):
    cod = ''
    neg = 1
    for bit in binario:
        cod += str(int(bit)*neg)
        if int(bit) == 1:
            neg *= -1
    return cod

def AMI_reverso(cod):
    binario = ''
    for i in cod:
        if i == '1' or i == '0':
            binario += i
    return binario


def grafico(cod):
    def exibir_grafico():
        graf = []
        i = 0
        while i < len(cod):
            if cod[i] == '0' or cod[i] == '1':
                graf.append(int(cod[i]))
            else:
                graf.append(-1)
                i+=1
            i+=1
        graf.append(graf[-1])
        plt.xticks(rotation=90)
        plt.step(range(len(graf)), graf, where='post')
        plt.title('AMI - Server')
        plt.xlabel('Tempo')
        plt.xticks(range(len(graf)))
        plt.ylabel('Amplitude')
        plt.grid()
        plt.show()

    base.after(100, exibir_grafico)

def start_receiver(host='0.0.0.0', port=5552):


    host = textbox_host.get("1.0", "end-1c")

    port = int(textbox_port.get("1.0", "end-1c"))


    receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    receiver_socket.bind((host, port))
    receiver_socket.listen(5)
    print(f"Servidor escutando em {host}:{port}...")

    sender_socket, sender_address = receiver_socket.accept()
    print(f"Conexão estabelecida com {sender_address}")

    key = sender_socket.recv(1024).decode()

    while server_var.get():
        if refresh.get():
            cod_linha = sender_socket.recv(1024).decode()
            print(cod_linha)
            grafico(cod_linha)
            cod_rev = AMI_reverso(cod_linha)
            label8.config(text = cod_rev)
            text = binario_para_texto(cod_rev)
            label2.config(text=(text))
            decrypted_message = xor_cipher(text, key)
            label4.config(text=decrypted_message)
            print(f"Recebido: {decrypted_message}")
            refresh.set(False)

    sender_socket.close()
    receiver_socket.close()

if __name__ == "__main__":
    thread = threading.Thread(target=start_receiver, daemon=True)
    base = tk.Tk()
    base.geometry("1000x1000")
    base.title("Server")

    label7 = tk.Label(base, width=90, height=1, text="Binário", font=('Arial', 18))
    label7.pack(padx=1, pady=1)

    label8 = tk.Label(base, width=90, height=2, text="", font=('Arial', 18), backgroun ='grey')
    label8.pack(padx=1, pady=1)

    label = tk.Label(base, text="Mensagem recebida criptografada", font=('Arial', 18))
    label.pack(padx=20, pady=20)

    label2 = tk.Label(base, height=5, width=70, text="    ", font=('Arial', 18), background='grey')
    label2.pack(padx=10, pady=10)

    label3 = tk.Label(base, text="Mensagem recebida descriptografada", font=('Arial', 18))
    label3.pack(padx=20, pady=20)

    label4 = tk.Label(base, width=90, height=5, text="    ", font=('Arial', 18), background='grey')
    label4.pack(padx=10, pady=10)

    refresh = tk.BooleanVar()
    btrefresh = tk.Button(base, text="Receber", command=recarregar)
    btrefresh.pack(pady=20)

    label5 = tk.Label(base, width=90, height=1, text="Host", font=('Arial', 18))
    label5.pack(padx=1, pady=1)

    textbox_host = tk.Text(base, height=1, font=('Arial', 18))
    textbox_host.pack(padx=20)

    label6 = tk.Label(base, width=90, height=1, text="Porta", font=('Arial', 18))
    label6.pack(padx=1, pady=1)

    textbox_port = tk.Text(base, height=1, font=('Arial', 18))
    textbox_port.pack(padx=20)

    server_var = tk.BooleanVar()
    check = tk.Checkbutton(base, text="Servidor", variable=server_var, command=toggle_server)
    check.pack()

    base.mainloop()
