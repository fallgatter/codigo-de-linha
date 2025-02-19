import matplotlib.pyplot as plt
import socket
import tkinter as tk
import threading

def enviar_mensagem():
    send_var.set(True)

def toggle_server(): 
    if server_var.get():
        if not thread.is_alive():
            thread.start()
            print("Servidor iniciado!")
    else:
        print("Servidor parado")

def xor_cipher(texto, chave): #Ideia retirada do Wikipedia
    resultado = ""
    for i, char in enumerate(texto):
        resultado += chr(ord(char) ^ ord(chave[i % len(chave)]))
    return resultado

def texto_para_binario(texto):
    binario = ''
    for char in texto:
        binario += '{:08b}'.format(ord(char)) #
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
        plt.title('AMI - Sender')
        plt.xlabel('Tempo')
        plt.xticks(range(len(graf)))
        plt.ylabel('Amplitude')
        plt.grid()
        plt.show()

    base.after(100, exibir_grafico)

def start_sender(receiver_host='0.0.0.0', receiver_port=5552): #Socket configurado com auxílio da documentação do Python e tópicos do StackOverflow

    receiver_host = textbox_host.get("1.0", "end-1c")

    receiver_port = int(textbox_port.get("1.0", "end-1c"))

    sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sender_socket.connect((receiver_host, receiver_port))

    key =  textbox_chave.get("1.0", "end-1c")

    sender_socket.send(key.encode())

    while server_var.get():
        if send_var.get():
            message = textbox.get("1.0", "end-1c")
            encrypted_message = xor_cipher(message, key)
            label3.config(text = encrypted_message)
            binary = texto_para_binario(encrypted_message)
            label5.config(text = str(binary))
            cod_linha = AMI(binary)
            send_var.set(False)
            grafico(cod_linha)
            print(cod_linha)
            sender_socket.send(cod_linha.encode())

    sender_socket.close()

if __name__ == "__main__":
    thread = threading.Thread(target=start_sender, daemon=True)

    base = tk.Tk()
    base.geometry("1000x700")
    base.title("Sender")

    label = tk.Label(base, text="Mensagem", font=('Arial', 18))
    label.pack(padx=20, pady=5)

    send_var = tk.BooleanVar()

    textbox = tk.Text(base, height=1, font=('Arial', 18))
    textbox.pack(padx=20)

    label8 = tk.Label(base, text="Chave", font=('Arial', 18))
    label8.pack(padx=20, pady=5)

    textbox_chave = tk.Text(base, height=1, font=('Arial', 18))
    textbox_chave.pack(padx=20)

    label2 = tk.Label(base, text="Mensagem criptografada", font=('Arial', 18))
    label2.pack(padx=20, pady=5)


    label3 = tk.Label(base, height=4, width=70, text="    ", font=('Arial', 18), background='grey')
    label3.pack(padx=10, pady=5)

    label4 = tk.Label(base, height = 1, text="Binário", font=('Arial', 18))
    label4.pack()

    label5 = tk.Label(base, height=4, width=70, text="    ", font=('Arial', 18), background='grey')
    label5.pack(padx=10, pady=5)

    button = tk.Button(base, text="Enviar", command=enviar_mensagem)
    button.pack(pady=5)

    label6 = tk.Label(base, width=90, height=1, text="Host", font=('Arial', 18))
    label6.pack(padx=1, pady=1)

    textbox_host = tk.Text(base, height=1, font=('Arial', 18))
    textbox_host.pack(padx=20)

    label7 = tk.Label(base, width=90, height=1, text="Porta", font=('Arial', 18))
    label7.pack(padx=1, pady=1)

    textbox_port = tk.Text(base, height=1, font=('Arial', 18))
    textbox_port.pack(padx=20)

    server_var = tk.BooleanVar()
    check = tk.Checkbutton(base, text="Servidor", variable=server_var, command=toggle_server)
    check.pack()

    base.mainloop() 
