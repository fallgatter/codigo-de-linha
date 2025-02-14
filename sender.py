from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import matplotlib.pyplot as plt
import socket
import tkinter as tk
import threading
import string

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
    for i in range(len(cod)):
        if cod[i] == '0' or cod[i] == '1':
            graf.append(int(cod[i]))
        else:
            graf.append(-1)
            i += 1    
    graf.append(graf[-1])
    plt.xticks(rotation=90)
    plt.step(range(len(graf)), graf, where='post')
    plt.title('AMI')
    plt.xlabel('Tempo')
    plt.xticks(range(len(graf)))
    plt.ylabel('Amplitude')
    plt.grid()
    plt.show()

def start_sender(receiver_host='172.20.10.8', receiver_port=5555):

    sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sender_socket.connect((receiver_host, receiver_port))

    message = "é os guri"
    #criptografar
    binary = texto_para_binario(message)
    cod_linha = AMI(binary)

    grafico(cod_linha)

    sender_socket.send(cod_linha.encode())

    sender_socket.close()

start_sender()

# grafico(cod_linha)
# cod_rev = AMI_reverso(cod_linha)
# text = binario_para_texto(cod_rev)
# #descriptografar
# print(text)