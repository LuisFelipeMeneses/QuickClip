import tkinter as tk
import socket
import threading
import os
import pyperclip
import keyboard as kb
import time
import json
import pickle

enviar = False

qntdCont = 0

class Application:

    def __init__(self, root):
        self.root = root
        self.fontePadrao = ("Arial", "10")

        self.contPrinc = tk.Frame(self.root, padx=10, pady=10)
        self.contPrinc.pack()
        criarBotao(self, self.contPrinc, "Host", self.host).pack(padx=10, side=tk.LEFT)
        criarBotao(self, self.contPrinc, "Client", self.client)

        self.mensagem = tk.Label(criarContainer(self, 10, 10), text="", font=self.fontePadrao)
        self.mensagem.pack()

    def host(self):
        limparConts(self)
        porta = criarTextoeCampo(self, "Porta", criarContainer(self, 10, 10))
        criarBotao(self, criarContainer(self, 10, 10), "Criar", lambda: runHost(self, int(porta.get())))
        self.txt = tk.Label(criarContainer(self, 10, 10), text="", font=self.fontePadrao)
        self.txt.pack()

    def client(self):
        limparConts(self)
        ip = criarTextoeCampo(self, "IP:", criarContainer(self, 10, 10))
        porta = criarTextoeCampo(self, "Porta:", criarContainer(self, 10, 10))
        nome = criarTextoeCampo(self, "Nome:", criarContainer(self, 10, 10))
        ip.pack(side=tk.BOTTOM)
        porta.pack(side=tk.BOTTOM)
        nome.pack(side=tk.BOTTOM)
        criarBotao(self, criarContainer(self, 10, 10), "Conectar", lambda: runClient(self, ip.get(), int(porta.get()), nome.get()))
        self.txt = tk.Label(criarContainer(self, 10, 10), text="", font=self.fontePadrao)
        self.txt.pack()

def criarBotao(self, cont, txt, func):
    btn = tk.Button(cont)
    btn["text"] = txt
    btn["font"] = ("Calibri", "8")
    btn["width"] = 12
    btn["command"] = func
    btn.pack()
    return btn

def criarTextoeCampo(self, txt, contn):
    texto = tk.Label(contn, text=txt, font=self.fontePadrao)
    texto.pack()
    campo = tk.Entry(contn)
    campo["width"] = 30
    campo["font"] = self.fontePadrao
    campo.pack(side=tk.LEFT)
    return campo

def criarContainer(self, padx, pady):
    global qntdCont
    novoCont = tk.Frame(self.root)
    novoCont["padx"] = padx
    novoCont["pady"] = pady
    novoCont.pack()
    nome = "cont" + str(qntdCont)
    setattr(self, nome, novoCont)
    qntdCont += 1
    return novoCont

def limparConts(self):
    global qntdCont
    for i in range(qntdCont):
        nome = "cont" + str(i)
        contNome = getattr(self, nome, None)
        if contNome is not None:  # Verifica se o container existe
            contNome.destroy()
            setattr(self, nome, None)  # Remove a referência ao container destruído
            qntdCont = 0  # Reseta o contador para evitar problemas

def runHost(self, porta):
    receive_thread = threading.Thread(target=lambda: hostServer(self, porta))
    receive_thread.start()

def runClient(self, ip, porta, nome):
    receive_thread = threading.Thread(target=lambda: clientServer(self, ip, porta, nome))
    receive_thread.start()

def hostServer(self, porta):
    HOST = 'seu ip'
    PORT = porta
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind((HOST, PORT))
    server.listen()
    print(f"Server escutando na porta: {PORT}")

    clients = []


    def sendMessage():
        global enviar
        if enviar == True:
            print("oxdga")
            if os.path.exists("areaTransf.json"):
                with open("areaTransf.json", "r") as arquivo:
                    dados = json.load(arquivo)
                    dadosEnviar = pickle.dumps(dados)
                for client in clients:
                    try:
                        client.sendall(dadosEnviar)  # Use sendall para garantir o envio completo
                    except BrokenPipeError:
                        print("Erro: Conexão perdida com o cliente.")
            else:
                print("Arquivo de transferência não encontrado.")
        enviar = False

    def handle(client, username):
        while True:
            try:
                sendMessage()
            except (EOFError, ConnectionResetError) as e:
                print(f"Erro ao enviar dados para o cliente: {e}")
                if client in clients:
                    clients.remove(client)
                client.close()
                break

    def receive():
        while True:
            client, address = server.accept()
            print(f"O usuário se conectou no servidor! endereço: {address}")
            clients.append(client)

            thread = threading.Thread(target=handle, args=(client, "username"), daemon=True)
            thread.start()

    def salvarTexto(self, n):
        if os.path.exists("areaTransf.json"):
            with open("areaTransf.json", "r") as arquivo:
                dados = json.load(arquivo)
        else:
            dados = {
                "dados": [{"id": 0, "dado": ""}, {"id": 1, "dado": ""}, {"id": 2, "dado": ""}, {"id": 3, "dado": ""}, {"id": 5, "dado": ""}, {"id": 6, "dado": ""}, {"id": 7, "dado": ""}, {"id": 8, "dado": ""}, {"id": 9, "dado": ""}]
            }

        dados["dados"][n]["dado"] = pyperclip.paste()
        with open("areaTransf.json", "w") as arquivo:
            json.dump(dados, arquivo, indent=4)
        self.txt["text"] = "Texto copiado para o arquivo"

    def copiarTexto(self, n):
        if os.path.exists("areaTransf.json"):
            with open("areaTransf.json", "r") as arquivo:
                pyperclip.copy(json.load(arquivo)["dados"][n]["dado"])
            self.txt["text"] = "Texto do arquivo salvo na área de transferência"
        else:
            self.txt["text"] = "Nenhum texto foi copiado, copie um antes"

    def detectar_tecla(self):
        while True:
            for i in range(9):
                if kb.is_pressed('ctrl+c+' + str(i)):
                    salvarTexto(self, i)
                    global enviar
                    enviar = True
                    print("asd")
                elif kb.is_pressed('shift+' + str(i) + '+v'):
                    copiarTexto(self, i)
            time.sleep(0.1)

    server_thread = threading.Thread(target=receive, daemon=True)
    server_thread.start()
    copyPaste = threading.Thread(target=detectar_tecla, args=(self,), daemon=True)
    copyPaste.start()

def clientServer(self, IP, Porta, Nome):
    HOST = IP
    PORT = Porta

    username = Nome
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    def receive():
        while True:
            try:
                dados = client.recv(1000000)
                if dados:
                    print(f"Dados recebidos: {dados[:100]}")  # Imprime uma parte dos dados para depuração
                    dadosConvert = pickle.loads(dados)
                    with open("areaTransf.json", "w") as arquivo:
                        json.dump(dadosConvert, arquivo, indent=4)
                else:
                    print("Conexão encerrada pelo servidor.")
                    break
            except (EOFError, pickle.UnpicklingError) as e:
                print(f"Erro ao desserializar dados: {e}")
                break

    def copiarTexto(self, n):
        if os.path.exists("areaTransf.json"):
            with open("areaTransf.json", "r") as arquivo:
                pyperclip.copy(json.load(arquivo)["dados"][n]["dado"])
            self.txt["text"] = "Texto do arquivo salvo na área de transferência"
        else:
            self.txt["text"] = "Nenhum texto foi copiado, copie um antes"

    def detectar_tecla(self):
        while True:
            for i in range(9):
                if kb.is_pressed('shift+' + str(i) + '+v'):
                    copiarTexto(self, i)
            time.sleep(0.1)

    receive_thread = threading.Thread(target=receive, daemon=True)
    receive_thread.start()

    copyPaste = threading.Thread(target=detectar_tecla, args=(self,), daemon=True)
    copyPaste.start()

root = tk.Tk()
Application(root)
root.geometry("640x360")
root.title("QuickClip")
root.mainloop()
