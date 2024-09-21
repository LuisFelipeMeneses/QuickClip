import customtkinter as ctk

class Aplication:
    def __init__(self, root):
        ctk.set_appearance_mode("dark")  # Modo escuro
        ctk.set_default_color_theme("dark-blue")  # Tema de cor padrão

        tabview = ctk.CTkTabview(root)
        tabview.pack(pady=5, padx=10, fill="both", expand=True)
        def_color = "#3b3b3b"

        tabview.add("Client")
        tabview.add("Server")

        client_frame = ctk.CTkFrame(tabview.tab("Client"), fg_color=def_color, width=300, height=150)
        client_frame.pack(pady=10, padx=10, fill="none")

        name_client = ctk.CTkEntry(client_frame, width=200, height=30, placeholder_text= "Name", font=("Arial", 16)).place(relx=0.5, rely=0.1, anchor="n")
        ip_client = ctk.CTkEntry(client_frame, width=200, height=30, placeholder_text= "IP", font=("Arial", 16)).place(relx=0.5, rely=0.4, anchor="n")
        port_client = ctk.CTkEntry(client_frame, width=200, height=30, placeholder_text= "Port", font=("Arial", 16)).place(relx=0.5, rely=0.7, anchor="n")

        btn_entry = ctk.CTkButton(tabview.tab("Client"), text="Join", command=lambda: print("OI"), font=("Arial",24))
        btn_entry.place(relx=0.5, rely=0.525, anchor="center")

        servers_frame = ctk.CTkScrollableFrame(tabview.tab("Client"), height= 100, label_text= "Servers List")
        servers_frame.place(relx = 0.5, rely = 0.6,anchor= "n")
        servers_frame._scrollbar.configure(height=0)

        for i in range(20):
            label = ctk.CTkLabel(servers_frame, text=f"Server {i + 1}")
            label.pack(pady=5)

        btn_entry = ctk.CTkButton(tabview.tab("Server"), text="Create", command=lambda: print("OI"), font=("Arial",24)).place(relx=0.5, rely=0.1, anchor="center")

        server_frame = ctk.CTkFrame(tabview.tab("Server"), fg_color=def_color, width=300, height=120)
        server_frame.pack(pady=80, padx=10, fill="none")

        server_advanced = ctk.CTkLabel(server_frame,text= "Advanced").place(relx = 0.5, rely = 0,anchor= "n")

        ip_server = ctk.CTkEntry(server_frame, width=200, height=30, placeholder_text= "IP", font=("Arial", 16)).place(relx=0.5, rely=0.3, anchor="n")
        port_server = ctk.CTkEntry(server_frame, width=200, height=30, placeholder_text= "Port", font=("Arial", 16)).place(relx=0.5, rely=0.7, anchor="n")

        self.frames = {}
        self.initialized_frames = set()
    def show_frame(self, cont, oldCont):
        if cont not in self.initialized_frames:
            if oldCont in self.frames:
                self.frames[oldCont].destroy()
                del self.frames[oldCont]
                self.initialized_frames.discard(oldCont)
            
            self.frames[cont] = cont(self.client_frame, self)
            self.frames[cont].grid(row=0, column=0, sticky="nsew")
            self.initialized_frames.add(cont)

root = ctk.CTk()
app = Aplication(root)
root.geometry("300x425")
root.title("QuickClip")
#root.resizable(False, False)
root.mainloop()
