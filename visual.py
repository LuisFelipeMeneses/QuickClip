import customtkinter as ctk
from CustomTkinterMessagebox import CTkMessagebox
import socket
import threading
import os
import pyperclip
import keyboard as kb
import time
import json
import pickle

enviar = False

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("QuickClip")
        self.geometry("300x425")

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True)

        self.screen_1_frame = ctk.CTkFrame(self)
        self.screen_2_frame = ctk.CTkFrame(self)

        self.server_ip = None
        self.server_port = None

        self.configure_main_screen()

    def configure_main_screen(self):
        tabview = ctk.CTkTabview(self.main_frame)
        tabview.pack(pady=5, padx=10, fill="both", expand=True)
        default_color = "#3b3b3b"

        tabview.add("Client")
        tabview.add("Server")

        client_frame = ctk.CTkFrame(tabview.tab("Client"), fg_color=default_color, width=300, height=150)
        client_frame.pack(pady=10, padx=10, fill="none")

        self.name_client_entry = ctk.CTkEntry(client_frame, width=200, height=30, placeholder_text="Name", font=("Arial", 16))
        self.name_client_entry.place(relx=0.5, rely=0.1, anchor="n")
        self.ip_client_entry = ctk.CTkEntry(client_frame, width=200, height=30, placeholder_text="IP", font=("Arial", 16))
        self.ip_client_entry.place(relx=0.5, rely=0.4, anchor="n")
        self.port_client_entry = ctk.CTkEntry(client_frame, width=200, height=30, placeholder_text="Port", font=("Arial", 16))
        self.port_client_entry.place(relx=0.5, rely=0.7, anchor="n")

        btn_entry = ctk.CTkButton(tabview.tab("Client"), text="Join", command= lambda: self.switch_to_screen_1(self.name_client_entry.get()), font=("Arial", 24))
        btn_entry.place(relx=0.5, rely=0.525, anchor="center")

        servers_frame = ctk.CTkScrollableFrame(tabview.tab("Client"), height=100, label_text="Servers List")
        servers_frame.place(relx=0.5, rely=0.6, anchor="n")
        servers_frame._scrollbar.configure(height=0)

        for i in range(20):
            label = ctk.CTkButton(servers_frame, text=f"Server {i + 1}", command= lambda: self.switch_to_screen_1(self.name_client_entry.get(), i, i), fg_color= "transparent")
            label.pack(pady=5)

        server_frame = ctk.CTkFrame(tabview.tab("Server"), fg_color=default_color, width=300, height=120)
        server_frame.pack(pady=80, padx=10, fill="none")

        ctk.CTkLabel(server_frame, text="Advanced").place(relx=0.5, rely=0, anchor="n")

        self.ip_server_entry = ctk.CTkEntry(server_frame, width=200, height=30, placeholder_text="IP", font=("Arial", 16))
        self.ip_server_entry.place(relx=0.5, rely=0.3, anchor="n")
        self.port_server_entry = ctk.CTkEntry(server_frame, width=200, height=30, placeholder_text="Port", font=("Arial", 16))
        self.port_server_entry.place(relx=0.5, rely=0.6, anchor="n")

        ctk.CTkButton(tabview.tab("Server"), text="Create", command= lambda: self.switch_to_screen_2(), font=("Arial", 24)).place(relx=0.5, rely=0.1, anchor="center")

    def switch_to_screen_1(self, name, ip=None, port=None):
        if not name:
            CTkMessagebox.messagebox(title='ERROR', text='Please enter a name before joining!', sound='on', button_text='OK')
        else:
            self.server_ip = ip
            self.server_port = port
            self.screen_1()

    def screen_1(self):
        self.switch_screen(self.screen_1_frame)
        self.reset_screen(self.screen_1_frame)
        ctk.CTkLabel(self.screen_1_frame, text=f"{self.name_client_entry.get()}, you have connected to the server!").place(relx=0.5, rely=0, anchor="n")
        ctk.CTkLabel(self.screen_1_frame, text=f"IP: {self.server_ip}:{self.server_port}").place(relx=0.5, rely=0.08, anchor="n")
        ctk.CTkButton(self.screen_1_frame, text="Disconnect", command=self.back_to_main, font=("Arial", 24)).place(relx=0.5, rely=0.2, anchor="center")

    def switch_to_screen_2(self, ip=None, port=None):
        self.server_ip = ip
        self.server_port = port
        self.screen_2()

    def screen_2(self):
        self.switch_screen(self.screen_2_frame)
        self.reset_screen(self.screen_2_frame)
        self.hostServer(self.server_ip,self.server_port)
        ctk.CTkLabel(self.screen_2_frame, text="Server Created!", font=("Arial", 24)).place(relx=0.5, rely=0.01, anchor="n")
        ctk.CTkLabel(self.screen_2_frame, text=f"IP: {self.server_ip}:{self.server_port}").place(relx=0.5, rely=0.94, anchor="n")
        ctk.CTkButton(self.screen_2_frame, text="Close Server", command= lambda: self.closeServer(self.server), font=("Arial", 24)).place(relx=0.5, rely=0.15, anchor="center")

        self.clients_frame = ctk.CTkScrollableFrame(self.screen_2_frame, height=220, label_text="Clients List")
        self.clients_frame.place(relx=0.5, rely=0.3, anchor="n")
        self.clients_frame._scrollbar.configure(height=0)

    def hostServer(self,ip= None, port= None):
        HOST = ip
        if not ip:
            HOST = socket.gethostbyname(socket.gethostname())
        if not port:
            PORT = 0
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverRunning = True
        self.server.bind((HOST, PORT))

        self.server.listen()
        HOST, PORT = self.server.getsockname()
        print(HOST)
        self.server_ip, self.server_port = HOST, PORT
        print(f"Server escutando na porta: {PORT}")
        clients = []
        usernames = []
        addresses = []

        broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # Habilita o modo broadcast

        def broadcast_announce():
            while self.serverRunning:
                try:
                    message = ["Servidor QuickClip disponível no IP: ", HOST, PORT]
                    broadcast_socket.sendto(pickle.dumps(message), ('<broadcast>', 37020))  # Envia broadcast para a rede
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
                    update_client_list(self,usernames)
                    break

        def receive(self):
            while self.serverRunning:
                try:
                    client, address = self.server.accept()
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
                    update_client_list(self,usernames)
                    break
                except OSError:
                    break
                #except Exception as e:
                    #print(f"Deu erro no sv: {e}")
                    #continue

        def update_client_list(self, usernames):
            try:
                self.clients_frame.destroy()
            except:
                pass
            self.clients_frame = ctk.CTkScrollableFrame(self.screen_2_frame, height=220, label_text="Clients List")
            self.clients_frame.place(relx=0.5, rely=0.3, anchor="n")
            self.clients_frame._scrollbar.configure(height=0)
            for index, username in enumerate(usernames):
                print("dfed")
                frame = ctk.CTkFrame(self.clients_frame, fg_color=self.clients_frame.cget("fg_color"))
                frame.pack(padx=5, pady=5, fill="x")

                text = ctk.CTkLabel(frame, text=f"{username}")
                text.grid(row=0, column=0, padx=5, pady=2, sticky="w")

                frame.grid_columnconfigure(0, weight=1)

                btn = ctk.CTkButton(frame, text="Remove", command=lambda user=username: frame.destroy(), width=70)
                btn.grid(row=0, column=1, padx=5, pady=2, sticky="e")

        def remove_client(self, username):
            print(f"Removing Client {username}")


        def salvarTexto(self, n):
            if os.path.exists("areaTransf.json"):
                with open("areaTransf.json", "r") as arquivo:
                    dados = json.load(arquivo)
            else:
                dados = {
                    "dados": [{"id": i, "dado": ""} for i in range(10)]
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

    def closeServer(self, server):
        self.serverRunning = False
        server.close()
        print("Servidor fechado!")
        self.back_to_main()

    def switch_screen(self, new_screen):
        self.main_frame.pack_forget()
        self.screen_1_frame.pack_forget()
        self.screen_2_frame.pack_forget()

        new_screen.pack(fill="both", expand=True)

    def reset_screen(self, screen):
        for widget in screen.winfo_children():
            widget.destroy()

    def back_to_main(self):
        self.screen_1_frame.pack_forget()
        self.screen_2_frame.pack_forget()
        self.main_frame.pack(fill="both", expand=True)

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    app = App()
    app.mainloop()