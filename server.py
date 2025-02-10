import matplotlib.pyplot as plt
import socket

def start_server(host='0.0.0.0', port=5555):
    # Cria um socket TCP/IP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Liga o socket ao endereço e porta
    server_socket.bind((host, port))
    
    # Escuta por conexões entrantes (max 5 conexões em espera)
    server_socket.listen(5)
    print(f"Servidor escutando em {host}:{port}...")
    
    # Aceita uma conexão
    client_socket, client_address = server_socket.accept()
    print(f"Conexão estabelecida com {client_address}")
    
    # Recebe dados do cliente
    data = client_socket.recv(1024)
    print(f"Recebido: {data.decode('utf-8')}")
    
    # Envia uma resposta
    client_socket.send(str('oi').encode())
    
    # Fecha a conexão
    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    start_server()

def texto_para_binario(texto):
    binario = ''
    for char in texto:
        binario += '{:08b}'.format(ord(char))
    return binario

def AMI(binario):
    cod = []
    neg = 1
    for bit in binario:
        cod.append(int(bit)*neg)
        if int(bit) == 1:
            neg *= -1
    return cod

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