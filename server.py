from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import matplotlib.pyplot as plt
import socket
import threading
import tkinter as tk
import threading

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
    plt.title('AMI')
    plt.xlabel('Tempo')
    plt.xticks(range(len(graf)))
    plt.ylabel('Amplitude')
    plt.grid()
    plt.show()

def start_receiver(host='172.20.10.8', port=5555):

    receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    receiver_socket.bind((host, port))

    receiver_socket.listen(5)
    print(f"Servidor escutando em {host}:{port}...")

    sender_socket, sender_address = receiver_socket.accept()
    print(f"Conexão estabelecida com {sender_address}")

    while server_var.get():
        if refresh.get():
            cod_linha = sender_socket.recv(1024).decode()
            key = sender_socket.recv(1024).decode()
            grafico(cod_linha)
            cod_rev = AMI_reverso(cod_linha)
            text = binario_para_texto(cod_rev)
            decrypted_message = xor_cipher(text, key)
            print(f"Recebido: {decrypted_message}")

    sender_socket.close()
    receiver_socket.close()

if __name__ == "__main__":
   # Criando a thread
    thread = threading.Thread(target=start_receiver, daemon=True)

    # Criando a interface gráfica
    base = tk.Tk()
    base.geometry("800x800")
    base.title("Receiver")

    label = tk.Label(base, text="Mensagem recebida pré criptografia", font=('Arial', 18))
    label.pack(padx=20, pady=20)

    label2 = tk.Label(base, height=5, width = 70, text="", font=('Arial', 18), background = 'grey')
    label2.pack(padx=10, pady=10)

    label3 = tk.Label(base, text="Mensagem recebida pós criptografia", font=('Arial', 18))
    label3.pack(padx=20, pady=20)

    label4 = tk.Label(base,  width = 90, height=5,text="", font=('Arial', 18), background = 'grey')
    label4.pack(padx=10, pady=10)


    refresh = tk.BooleanVar()
    btrefresh = tk.Button(base, text="receber", command=recarregar)
    btrefresh.pack(pady=20)

    # Checkbutton para ativar/desativar o servidor
    server_var = tk.BooleanVar()
    check = tk.Checkbutton(base, text="Servidor", variable=server_var, command=toggle_server)
    check.pack()

    base.mainloop()



