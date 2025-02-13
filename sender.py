from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import matplotlib.pyplot as plt
import socket

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

def start_sender(receiver_host='192.168.1.100', receiver_port=12345):
    rsa = RSA()
    message = 'oi'
    sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sender_socket.connect((receiver_host, receiver_port))

    public_key_pem = sender_socket.recv(1024)
    public_key = serialization.load_pem_public_key(public_key_pem)
    encrypted_message = rsa.encrypt(message, public_key)
    binary = texto_para_binario(encrypted_message)
    AMI = AMI(binary)

    grafico(AMI)
    sender_socket.send(AMI)

    sender_socket.close()

if __name__ == "__main__":
    start_sender()


