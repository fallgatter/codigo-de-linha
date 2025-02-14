from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import matplotlib.pyplot as plt
import socket
import threading
import tkinter as tk
import threading


def recarregar():
    refresh.set(True)

def toggle_server():
    if server_var.get():
        if not thread.is_alive():
            thread.start()
            print("Servidor iniciado!")
    else:
        print("Servidor parado")


class RSA:
    def __init__(self):
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.public_key = self.private_key.public_key()

    def encrypt(self, message, public_key):
        encrypted_message = public_key.encrypt(
            message.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return encrypted_message

    def decrypt(self, encrypted_message) -> bytes:
        decrypted_message = self.private_key.decrypt(
            encrypted_message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted_message

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
    cod = []
    neg = 1
    for bit in binario:
        cod.append(int(bit)*neg)
        if int(bit) == 1:
            neg *= -1
    return cod

def AMI_reverso(cod):
    binario = ''
    for i in cod:
        if i == -1:
            binario += '1'
        else:
            binario += str(i)
    return binario

def grafico(cod):
    graf = cod.copy()
    graf.append(graf[-1])
    plt.step(range(len(graf)), graf, where='post')
    plt.title('AMI')
    plt.xlabel('Tempo')
    plt.xticks(range(len(graf)))
    plt.ylabel('Amplitude')
    plt.grid()
    plt.show()

def start_receiver(host='0.0.0.0', port=5555):
    rsa = RSA()

    receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    receiver_socket.bind((host, port))

    receiver_socket.listen(5)
    print(f"Servidor escutando em {host}:{port}...")

    sender_socket, sender_address = receiver_socket.accept()
    print(f"Conexão estabelecida com {sender_address}")

    sender_socket.send(rsa.public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ))


    while server_var.get():
        if refresh.get():
            encrypted_message = sender_socket.recv(1024)
            grafico(encrypted_message)
            binary = AMI_reverso(encrypted_message)
            message = binario_para_texto(binary)
            decrypted_message = rsa.decrypt(message)
            print(decrypted_message)
            label2.config(text = decrypted_message)
            refresh.set(False)


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

    label4 = tk.Label(base,  width = 70, height=5,text="", font=('Arial', 18), background = 'grey')
    label4.pack(padx=10, pady=10)


    refresh = tk.BooleanVar()
    btrefresh = tk.Button(base, text="receber", command=recarregar)
    btrefresh.pack(pady=20)

    # Checkbutton para ativar/desativar o servidor
    server_var = tk.BooleanVar()
    check = tk.Checkbutton(base, text="Servidor", variable=server_var, command=toggle_server)
    check.pack()

    base.mainloop()



