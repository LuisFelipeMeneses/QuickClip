import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("QuickClip")
        self.geometry("300x425")

        # Criação dos frames
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True)

        self.tela_1_frame = ctk.CTkFrame(self)
        self.tela_2_frame = ctk.CTkFrame(self)

        # Campo de texto para a tela principal

        self.server_ip = None
        self.server_port = None

        self._configura_tela_principal()

    def _configura_tela_principal(self):
        tabview = ctk.CTkTabview(self.main_frame)
        tabview.pack(pady=5, padx=10, fill="both", expand=True)
        def_color = "#3b3b3b"

        tabview.add("Client")
        tabview.add("Server")

        client_frame = ctk.CTkFrame(tabview.tab("Client"), fg_color=def_color, width=300, height=150)
        client_frame.pack(pady=10, padx=10, fill="none")

        self.name_client = ctk.CTkEntry(client_frame, width=200, height=30, placeholder_text="Name", font=("Arial", 16))
        self.name_client.place(relx=0.5, rely=0.1, anchor="n")
        self.ip_client = ctk.CTkEntry(client_frame, width=200, height=30, placeholder_text="IP", font=("Arial", 16))
        self.ip_client.place(relx=0.5, rely=0.4, anchor="n")
        self.port_client = ctk.CTkEntry(client_frame, width=200, height=30, placeholder_text="Port", font=("Arial", 16))
        self.port_client.place(relx=0.5, rely=0.7, anchor="n")

        btn_entry = ctk.CTkButton(tabview.tab("Client"), text="Join", command= self.mudar_para_tela_1, font=("Arial", 24))
        btn_entry.place(relx=0.5, rely=0.525, anchor="center")

        servers_frame = ctk.CTkScrollableFrame(tabview.tab("Client"), height=100, label_text="Servers List")
        servers_frame.place(relx=0.5, rely=0.6, anchor="n")
        servers_frame._scrollbar.configure(height=0)

        for i in range(20):
            label = ctk.CTkLabel(servers_frame, text=f"Server {i + 1}")
            label.pack(pady=5)

        server_frame = ctk.CTkFrame(tabview.tab("Server"), fg_color=def_color, width=300, height=120)
        server_frame.pack(pady=80, padx=10, fill="none")

        server_advanced = ctk.CTkLabel(server_frame, text="Advanced").place(relx=0.5, rely=0, anchor="n")

        self.ip_server = ctk.CTkEntry(server_frame, width=200, height=30, placeholder_text="IP", font=("Arial", 16))
        self.ip_server.place(relx=0.5, rely=0.3, anchor="n")
        self.port_server = ctk.CTkEntry(server_frame, width=200, height=30, placeholder_text="Port", font=("Arial", 16))
        self.port_server.place(relx=0.5, rely=0.6, anchor="n")

        btn_entry = ctk.CTkButton(tabview.tab("Server"), text="Create", command= self.mudar_para_tela_2, font=("Arial", 24)).place(relx=0.5, rely=0.1, anchor="center")

    def mudar_para_tela_1(self):
        self._mudar_tela(self.tela_1_frame)
        self._resetar_tela(self.tela_1_frame)  # Resetar tela 1
        self.server_ip = self.ip_client.get()
        self.server_port = self.port_client.get()
        ctk.CTkLabel(self.tela_1_frame, text=f"{self.name_client.get()}, você se conectou ao servidor!").place(relx=0.5, rely=0, anchor="n")
        ctk.CTkLabel(self.tela_1_frame, text=f"IP: {self.server_ip}:{self.server_port}").place(relx=0.5, rely=0.08, anchor="n")
        ctk.CTkButton(self.tela_1_frame, text="Desconectar", command= self.voltar, font=("Arial", 24)).place(relx=0.5, rely=0.2, anchor="center")

    def mudar_para_tela_2(self):
        self._mudar_tela(self.tela_2_frame)
        self._resetar_tela(self.tela_2_frame)  # Resetar tela 2
        ctk.CTkLabel(self.tela_2_frame, text="Servidor Criado!", font=("Arial",24)).place(relx=0.5, rely=0.01, anchor="n")
        self.server_ip = self.ip_server.get()
        self.server_port = self.port_server.get()
        ctk.CTkLabel(self.tela_2_frame, text=f"IP: {self.server_ip}:{self.server_port}").place(relx=0.5, rely=0.94, anchor="n")
        btn_entry = ctk.CTkButton(self.tela_2_frame, text="Close Server", command= self.voltar, font=("Arial", 24)).place(relx=0.5, rely=0.15, anchor="center")

        clients_frame = ctk.CTkScrollableFrame(self.tela_2_frame, height=220, label_text="Clients List")
        clients_frame.place(relx=0.5, rely=0.3, anchor="n")
        clients_frame._scrollbar.configure(height=0)

        for i in range(20):
            frame = ctk.CTkFrame(clients_frame, fg_color= clients_frame.cget("fg_color"))
            frame.pack(padx=5, pady=5, fill="x")

            text = ctk.CTkLabel(frame, text=f"Client {i + 1}")
            text.grid(row=0, column=0, padx=5, pady=2, sticky="w")

            frame.grid_columnconfigure(0, weight=1)

            btn = ctk.CTkButton(frame, text="Remover", command=lambda i=i: print(f"Removendo Cliente {i + 1}"), width=70)
            btn.grid(row=0, column=1, padx=5, pady=2, sticky="e")

    def _mudar_tela(self, nova_tela):
        # Esconde todas as telas e mostra a nova
        self.main_frame.pack_forget()
        self.tela_1_frame.pack_forget()
        self.tela_2_frame.pack_forget()

        nova_tela.pack(fill="both", expand=True)

    def _resetar_tela(self, tela):
        # Limpa os elementos da tela
        for widget in tela.winfo_children():
            widget.destroy()

    def voltar(self):
        # Volta para a tela principal
        self.tela_1_frame.pack_forget()
        self.tela_2_frame.pack_forget()
        self.main_frame.pack(fill="both", expand=True)

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")  # Modo escuro
    ctk.set_default_color_theme("dark-blue")  # Tema azul
    app = App()
    app.mainloop()