from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import matplotlib.pyplot as plt
import socket
import tkinter as tk
import threading
import string

def enviar_mensagem():
    send_var.set(True)

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
    return ''.join(f'{ord(char):08b}' for char in texto)

def binario_para_texto(binario):
    return ''.join(chr(int(binario[i:i+8], 2)) for i in range(0, len(binario), 8))

def AMI(binario):
    cod = []
    neg = 1
    for bit in binario:
        cod.append(int(bit)*neg)
        if int(bit) == 1:
            neg *= -1
    return cod

def AMI_reverso(cod):
    return ''.join('1' if i == -1 else str(i) for i in cod)

def grafico(cod):
    graf = cod.copy()
    graf.append(graf[-1] if graf else 0)
    plt.step(range(len(graf)), graf, where='post')
    plt.title('AMI')
    plt.xlabel('Tempo')
    plt.xticks(range(len(graf)))
    plt.ylabel('Amplitude')
    plt.grid()
    plt.show()

def start_sender(receiver_host='0.0.0.0', receiver_port=5555):
    rsa = RSA()

    sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sender_socket.connect((receiver_host, receiver_port))


    public_key_pem = sender_socket.recv(1024)
    public_key = serialization.load_pem_public_key(public_key_pem)

    while server_var.get():
        if send_var.get():
            message = textbox.get("1.0", "end-1c")
                # Converte a string binária para bytes

            encrypted_message = rsa.encrypt(message, public_key)
            print(type(encrypted_message))
            print((encrypted_message))
            print((encrypted_message).hex().upper())
            binary = texto_para_binario((encrypted_message).hex().upper())
            cacete = AMI(binary)
            print(binary)
            print(cacete)
            # grafico(AMI)
            sender_socket.send(str(cacete).encode)
            print(cacete)

            send_var.set(False)

    sender_socket.close()

if __name__ == "__main__":
    # Criando a thread da comunicação
    thread = threading.Thread(target=start_sender, daemon=True)

    # Criando a interface gráfica
    base = tk.Tk()
    base.geometry("500x500")
    base.title("Receiver")

    # Criando a label de indentificação
    label = tk.Label(base, text="Digite sua mensagem", font=('Arial', 18))
    label.pack(padx=20, pady=20)

    # Criando a variável de envio
    send_var = tk.BooleanVar()

    # Criando a caixa de texto que o usuário preenche
    textbox = tk.Text(base, height=1, font=('Arial', 18))
    textbox.pack(padx=20)

    # Criando o button que o usuário vai clicar para enviar
    button = tk.Button(base, text="Enviar", command=enviar_mensagem)
    button.pack(pady=20)

    # Checkbutton para ativar/desativar o servidor
    server_var = tk.BooleanVar()
    check = tk.Checkbutton(base, text="Servidor", variable=server_var, command=toggle_server)
    check.pack()

    # Loop principal
    base.mainloop()
