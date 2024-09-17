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

class Application:

    def __init__(self, root):
        self.root = root
        self.fontePadrao = ("Arial", "10")
        
        self.mainContainer = tk.Frame(self.root)
        self.mainContainer.pack(fill="y", expand=True)

        self.frames = {}
        self.initialized_frames = set()

        self.serverPort = None
        self.serverIP = None
        self.name = None
        
        # Inicialize apenas o frame principal
        self.frames[MainScreen] = MainScreen(self.mainContainer, self)
        self.frames[MainScreen].grid(row=0, column=0, sticky="nsew")
        self.show_frame(MainScreen, MainScreen)

    def show_frame(self, cont, oldCont):
        if cont not in self.initialized_frames:
            if oldCont in self.frames:
                self.frames[oldCont].destroy()
                del self.frames[oldCont]
                self.initialized_frames.discard(oldCont)
            
            self.frames[cont] = cont(self.mainContainer, self)
            self.frames[cont].grid(row=0, column=0, sticky="nsew")
            self.initialized_frames.add(cont)
        
        frame = self.frames[cont]
        frame.tkraise()

class BaseScreen(tk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.controller = controller
        self.fontePadrao = ("Arial", "10")
        self.containers = []

    def fieldAndTextCreate(self, txt=None, container=None, fieldCreate=False, sideText=tk.TOP, padx=5, pady=5):
        if container is None:
            container = self.containerCreate()
        text = tk.Label(container, text=txt, font=self.fontePadrao).pack(side=sideText, padx=padx, pady=pady)
        if fieldCreate:
            field = tk.Entry(container)
            return field
        else:
            return text

    def containerCreate(self, addToList=True, side=tk.TOP, padx=10, pady=10):
        container = tk.Frame(self, padx=padx, pady=pady)
        container.pack(side=side)
        if addToList:
            self.containers.append(container)
        return container

    def containersDestroy(self):
        for container in self.containers:
            container.destroy()
        self.containers = []

    def buttomCreate(self, txt, container, func, side=tk.TOP, font=None, width=10, padx=10, pady=10):
        if font is None:
            font = self.fontePadrao
        return tk.Button(container, text=txt, font=font, width=width, command=func).pack(side=side, padx=padx, pady=pady)

    def nullFunc(self):
        print("")

class MainScreen(BaseScreen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        mainContainer = self.containerCreate(0)
        self.buttomCreate("Server", mainContainer, lambda: self.server(controller), tk.LEFT)
        self.buttomCreate("Client", mainContainer, lambda: self.client(controller), tk.LEFT)
        self.fieldAndTextCreate("Seja bem vindo ao QuickClip!")
        self.serverAddr = None
        self.serverIPloc = None
        self.serverPortloc = None
        self.is_server = False

    def discover_servers(self):
        if self.is_server:
            print("Esta instância é um servidor, não iniciando a busca de servidores.")
            return
        
        broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        broadcast_socket.settimeout(10)
        broadcast_socket.bind(('', 37020))  # Porta 37020 é usada para escutar broadcasts
            
        try:
            while True:
                data, self.serverAddr = broadcast_socket.recvfrom(1024)  # Recebe os pacotes de broadcast
                self.serverIPloc, self.serverPortloc = self.serverAddr
                message = data.decode('utf-8')
                print(f"Servidor descoberto: {message}")
                
                # Aqui, você pode preencher campos de IP e Porta automaticamente
        except socket.timeout:
            print("Nenhum servidor encontrado.")

    def server(self, controller):
        self.is_server = True
        self.containersDestroy()
        serverContainer = self.containerCreate()
        self.buttomCreate("Create", serverContainer, lambda: self.createServer(controller, 0))
        self.buttomCreate("Advanced", serverContainer, lambda: self.advancedSettings(controller))
        
    def advancedSettings(self, controller):
        self.containersDestroy()
        serverContainer = self.containerCreate()
        port = self.fieldAndTextCreate("Port", serverContainer, 1)
        port.pack()
        self.buttomCreate("Create", serverContainer, lambda: self.createServer(controller, int(port.get())))
        self.buttomCreate("Advanced", serverContainer, lambda: self.server(controller))

    def createServer(self, controller, port=None):
        controller.serverPort = port
        controller.show_frame(serverCreatedScreen, MainScreen)

    def client(self, controller):
        self.is_server = False
        self.containersDestroy()
        clientContainer = self.containerCreate()
        ip = self.fieldAndTextCreate("IP", clientContainer, 1, tk.TOP)
        ip.pack()
        port = self.fieldAndTextCreate("Port", clientContainer, 1, tk.TOP)
        port.pack()
        name = self.fieldAndTextCreate("Name", clientContainer, 1, tk.TOP)
        name.pack()
        self.buttomCreate("Join", clientContainer, lambda: self.clientConnecting(controller, ip.get(), int(port.get()), name.get()))
        
        discovery_thread = threading.Thread(target=self.discover_servers, daemon=True)
        discovery_thread.start()

    def clientConnecting(self, controller, ip, port, name):
        controller.serverIP = ip
        controller.serverPort = port
        controller.name = name
        controller.show_frame(clientConnectedScreen, MainScreen)

class clientConnectedScreen(BaseScreen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.clientInServer = True
        self.clientServer(controller, controller.serverIP, controller.serverPort, controller.name)

    def clientDisconnect(self, controller, client):
        self.clientInServer = False
        try:
            client.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        finally:
            client.close()
        controller.show_frame(MainScreen, clientConnectedScreen)

    def clientServer(self, controller, ip, port, name):
        HOST = ip
        PORT = port

        username = name.encode("utf-8")
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))
        client.send(username)
        self.clientInServer = True

        clientContainer = self.containerCreate()
        self.fieldAndTextCreate("Você se conectou ao servidor!", clientContainer)
        self.buttomCreate("Disconnect", clientContainer, lambda: self.clientDisconnect(controller, client))

        def receive():
            while self.clientInServer:
                try:
                    dados = client.recv(1000000)
                    try:
                        dados.decode("utf-8")
                        continue
                    except:
                        if dados:
                            dadosConvert = pickle.loads(dados)
                            with open("areaTransf.json", "w") as arquivo:
                                json.dump(dadosConvert, arquivo, indent=4)
                        else:
                            break
                except (EOFError, pickle.UnpicklingError) as e:
                    print(f"Erro ao desserializar dados: {e}")
                    break
                except Exception:
                    print("Desconectado")
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

class serverCreatedScreen(BaseScreen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        serverPort = controller.serverPort
        self.serverRunning = False
        self.hostServer(controller, serverPort)

    def hostServer(self, controller, porta):
        HOST = socket.gethostbyname(socket.gethostname())
        PORT = porta
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverRunning = True

        server.bind((HOST, PORT))
        server.listen()
        HOST, PORT = server.getsockname()
        print(f"Server escutando na porta: {PORT}")
        clients = []
        usernames = []
        addresses = []

        clientContainer = self.containerCreate(0)
        self.fieldAndTextCreate("Server Created", clientContainer)
        self.portaServer = tk.Label(clientContainer, text=f"IP: {HOST}: {PORT}", font=self.fontePadrao)
        self.portaServer.pack(side=tk.TOP)
        self.buttomCreate("Close Server", clientContainer, lambda: self.closeServer(controller, server))
        self.fieldAndTextCreate("Clients List: ", clientContainer)
        self.clientsListContainer = self.containerCreate()
        broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # Habilita o modo broadcast

        def broadcast_announce():
            while self.serverRunning:
                try:
                    message = f"Servidor disponível no IP {HOST}, Porta {PORT}"
                    broadcast_socket.sendto(message.encode('utf-8'), ('<broadcast>', 37020))  # Envia broadcast para a rede
                    time.sleep(5)  # Envia a cada 5 segundos
                except Exception as e:
                    print(f"Erro ao enviar broadcast: {e}")
                    break
        
        # Thread para envio de broadcast
        broadcast_thread = threading.Thread(target=broadcast_announce, daemon=True)
        broadcast_thread.start()

        def sendMessage(client):
            client.send("CONNECTION_TEST".encode("utf-8"))
            global enviar
            if enviar == True:
                if os.path.exists("areaTransf.json"):
                    with open("areaTransf.json", "r") as arquivo:
                        dados = json.load(arquivo)
                        dadosEnviar = pickle.dumps(dados)
                        try:
                            client.sendall(dadosEnviar)  # Use sendall para garantir o envio completo
                        except BrokenPipeError:
                            print("Erro: Conexão perdida com o cliente.")
                else:
                    print("Arquivo de transferência não encontrado.")
                enviar = False
            time.sleep(0.2)

        def handle(self, client, username, address):
            while True:
                try:
                    sendMessage(client)
                except:
                    print(f"Usuário: {username} desconectado")
                    if client in clients:
                        clients.remove(client)
                    if username in usernames:
                        usernames.remove(username)
                    if address in addresses:
                        addresses.remove(address)
                    client.close()
                    self.containersDestroy()
                    self.clientsListContainer = self.containerCreate()
                    for username in range(len(usernames)):
                        self.fieldAndTextCreate(usernames[username], self.clientsListContainer)
                    break

        def receive(self):
            while self.serverRunning:
                try:
                    client, address = server.accept()
                    if address[0] in addresses:
                        addresses.remove(address[0])
                        print("Usuario repetido removido")
                        if client in clients:
                            clients.remove(client)
                        if username in usernames:
                            usernames.remove(username)
                        client.close()
                    username = client.recv(1024).decode("utf-8")
                    print(f"O {username} se conectou no servidor! endereço: {address}")
                    clients.append(client)
                    usernames.append(username)
                    addresses.append(address[0])
                    thread = threading.Thread(target=handle, args=(self, client, username, address[0]), daemon=True)
                    thread.start()
                    self.containersDestroy()
                    self.clientsListContainer = self.containerCreate()
                    for username in usernames:
                        self.fieldAndTextCreate(username, self.clientsListContainer)
                except OSError:
                    break
                except Exception as e:
                    print(f"Deu erro no sv: {e}")
                    continue

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

        def copiarTexto(self, n):
            if os.path.exists("areaTransf.json"):
                with open("areaTransf.json", "r") as arquivo:
                    pyperclip.copy(json.load(arquivo)["dados"][n]["dado"])

        def detectar_tecla(self):
            while True:
                for i in range(9):
                    if kb.is_pressed('ctrl+c+' + str(i)):
                        salvarTexto(self, i)
                        global enviar
                        enviar = True
                    elif kb.is_pressed('shift+' + str(i) + '+v'):
                        copiarTexto(self, i)
                time.sleep(0.1)

        server_thread = threading.Thread(target=receive, args=(self,), daemon=True)
        server_thread.start()
        copyPaste = threading.Thread(target=detectar_tecla, args=(self,), daemon=True)
        copyPaste.start()

    def closeServer(self, controller, server):
        self.serverRunning = False
        server.close()
        print("Servidor fechado!")
        controller.show_frame(MainScreen, serverCreatedScreen)

root = tk.Tk()
app = Application(root)
root.geometry("640x360")
root.title("QuickClip")
root.mainloop()
