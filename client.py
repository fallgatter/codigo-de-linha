import matplotlib.pyplot as plt
import socket

def start_client(server_host='192.168.1.100', server_port=12345):
    # Cria um socket TCP/IP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Conecta ao servidor
    client_socket.connect((server_host, server_port))
    print(f"Conectado ao servidor {server_host}:{server_port}")
    
    # Envia dados ao servidor
    message = "Olá, servidor!"
    client_socket.send(message.encode('utf-8'))
    
    # Recebe a resposta do servidor
    data = client_socket.recv(1024)
    print(f"Recebido: {data.decode('utf-8')}")
    
    # Fecha a conexão
    client_socket.close()

if __name__ == "__main__":
    start_client()

def binario_para_texto(binario):
    texto = ''
    for bit in range(0, len(binario), 8):
        texto += chr(int(binario[bit:bit+8], 2))
    return texto

def AMI_reverso(cod):
    binario = ''
    for i in cod:
        if i == -1:
            binario += '1'
        else:
            binario += str(i)
    return binario