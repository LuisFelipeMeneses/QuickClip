from tkinter import *
import pyperclip
import keyboard as kb
import threading
import time
import os 
import json

class Application:
    def __init__(self, master=None):
        self.fontePadrao = ("Arial", "10")
        self.Container = Frame(master)
        self.Container["padx"] = 100
        self.Container.pack()

        self.Containery = Frame(master)
        self.Containery["pady"] = 10
        self.Containery.pack()

        self.titulo = Label(self.Container, text="QuickClip", pady=5)
        self.titulo["font"] = ("Arial", "30", "bold")
        self.titulo.pack()

        self.salvar = Button(self.Containery)
        self.salvar["text"] = "Salvar"
        self.salvar["font"] = ("Calibri", "15")
        self.salvar["width"] = 12
        self.salvar["command"] = lambda: self.salvarTexto(0)
        self.salvar.pack()

        self.copiar = Button(self.Container)
        self.copiar["text"] = "Copiar"
        self.copiar["font"] = ("Calibri", "15")
        self.copiar["width"] = 12
        self.copiar["command"] = lambda: self.copiarTexto(0)
        self.copiar.pack()

        self.mensagem = Label(self.Containery, text="", font=self.fontePadrao)
        self.mensagem.pack()

        # Iniciar a detecção de tecla em um thread separado
        self.iniciar_detecao_tecla()

    def salvarTexto(self,n):  
        if os.path.exists("areaTransf.json"):
            with open("areaTransf.json", "r") as arquivo:     
                dados = json.load(arquivo)
        else:
            dados = {
                "dados": [{"id": 0,"dado": ""},{"id": 1,"dado": ""},{"id": 2,"dado": ""},{"id": 3,"dado": ""},{"id": 5,"dado": ""},{"id": 6,"dado": ""},{"id": 7,"dado": ""},{"id": 8,"dado": ""},{"id": 9,"dado": ""}]}
                
        dados["dados"][n]["dado"] = pyperclip.paste()
        with open("areaTransf.json", "w") as arquivo:     
            json.dump(dados,arquivo, indent=1)
        self.mensagem["text"] = "Texto copiado para o arquivo"

    def copiarTexto(self,n):
        if os.path.exists("areaTransf.json"):
            arquivo = open("areaTransf.json", "r")
            pyperclip.copy(json.load(arquivo)["dados"][n]["dado"])
            self.mensagem["text"] = "Texto do arquivo salvo na área de transferência"
        else:
            self.mensagem["text"] = "Nenhum texto foi copiado, copie um antes"

    def detectar_tecla(self):
        while True:
            for i in range(9):
                if kb.is_pressed('ctrl+c+' + str(i)):
                    self.salvarTexto(i)
                elif kb.is_pressed('shift+' + str(i) + '+v'):
                    self.copiarTexto(i)
            time.sleep(0.1)

    def iniciar_detecao_tecla(self):
        # Usar thread para não bloquear o Tkinter mainloop
        t = threading.Thread(target=self.detectar_tecla, daemon=True)
        t.start()


root = Tk()
Application(root)
root.mainloop()