import matplotlib.pyplot as plt

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
        if bit == '0':
            cod.append(0)
        elif bit == '1':
            cod.append(neg)
            neg *= -1
    cod.append(cod[-1])
    return cod

def grafico(cod):
    plt.step(range(len(cod)), cod, where='post')
    plt.title('AMI')
    plt.xlabel('Tempo')
    plt.xticks(range(len(cod)))
    plt.ylabel('Amplitude')
    plt.grid()
    plt.show()

texto = 'Oiê'

binario= texto_para_binario(texto)

print(binario)

ami= AMI(binario)

grafico(ami)

print(ami)

texto = binario_para_texto(binario)

print(texto)