from tkinter import *
import pyperclip
import keyboard as kb
import threading
import time

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
        self.salvar["command"] = self.salvarTexto
        self.salvar.pack()

        self.copiar = Button(self.Container)
        self.copiar["text"] = "Copiar"
        self.copiar["font"] = ("Calibri", "15")
        self.copiar["width"] = 12
        self.copiar["command"] = self.copiarTexto
        self.copiar.pack()

        self.mensagem = Label(self.Containery, text="", font=self.fontePadrao)
        self.mensagem.pack()

        # Iniciar a detecção de tecla em um thread separado
        self.iniciar_detecao_tecla()

    def salvarTexto(self):
        arquivo = open("areaTransf.txt", "w")
        arquivo.write(pyperclip.paste())
        arquivo.close()
        self.mensagem["text"] = "Texto salvo no arquivo"

    def copiarTexto(self):
        arquivo = open("areaTransf.txt", "r")
        pyperclip.copy(arquivo.read())
        arquivo.close()
        self.mensagem["text"] = "Texto do arquivo salvo na área de transferência"

    def detectar_tecla(self):
        while True:
            if kb.is_pressed('shift+1+c'):
                self.salvarTexto()
            elif kb.is_pressed('shift+1+v'):
                self.copiarTexto()
            time.sleep(0.1)

    def iniciar_detecao_tecla(self):
        # Usar thread para não bloquear o Tkinter mainloop
        t = threading.Thread(target=self.detectar_tecla, daemon=True)
        t.start()


root = Tk()
Application(root)
root.mainloop()