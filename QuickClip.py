import tkinter as tk
import socket
import threading
import os
import pyperclip
import keyboard as kb
import time
import json
import pickle

class Application:

    def __init__(self, root):
        self.root = root
        self.fontePadrao = ("Arial", "10")
        
        self.mainContainer = tk.Frame(self.root)
        self.mainContainer.pack(fill="y", expand=True)

        self.frames = {}
        for F in (MainScreen, clientConnectedScreen, serverCreatedScreen):
            frame = F(self.mainContainer, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(MainScreen)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class BaseScreen(tk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.controller = controller
        self.fontePadrao = ("Arial", "10")
        self.containers = []

    def fieldAndTextCreate(self,txt=None,container=None, fieldCreate=False, sideText=tk.TOP,padx= 5, pady = 5):
        if container is None:
            container = self.containerCreate()
        text = tk.Label(container, text=txt, font=self.fontePadrao).pack(side=sideText, padx= padx, pady= pady)
        if fieldCreate:
            field = tk.Entry(container)
            return field
        else:
            return text

    def containerCreate(self, addToList = True, side=tk.TOP, padx=10, pady=10):
        container = tk.Frame(self, padx=padx, pady=pady)
        container.pack(side=side)
        if addToList:
            self.containers.append(container)
        return container

    def containersDestroy(self):
        for container in self.containers:
            container.destroy()
        self.containers = []

    def buttomCreate(self,txt, container, func, side=tk.TOP, font=None, width=10, padx= 10, pady = 10):
        if font is None:
            font = self.fontePadrao
        return tk.Button(container, text=txt, font=font, width=width, command= func).pack(side=side, padx= padx, pady= pady)

    def nullFunc(self):
        print("")

class MainScreen(BaseScreen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        mainContainer = self.containerCreate(0)
        self.buttomCreate("Server",mainContainer, lambda: self.server(controller),tk.LEFT)
        self.buttomCreate("Client",mainContainer, lambda: self.client(controller), tk.LEFT)
        self.fieldAndTextCreate("Seja bem vindo ao QuickClip!")

    def server(self,controller):
        self.containersDestroy()
        serverContainer = self.containerCreate()
        self.buttomCreate("Create",serverContainer,lambda: controller.show_frame(serverCreatedScreen))
        self.buttomCreate("Advanced",serverContainer,lambda: self.advancedSettings(controller))
        
    def advancedSettings(self,controller):
        self.containersDestroy()
        serverContainer = self.containerCreate()
        port = self.fieldAndTextCreate("Port",serverContainer,1)
        port.pack()
        self.buttomCreate("Create",serverContainer,lambda: controller.show_frame(serverCreatedScreen))
        self.buttomCreate("Advanced",serverContainer,lambda: self.server(controller))

    def client(self,controller):
        self.containersDestroy()
        clientContainer = self.containerCreate()
        ip = self.fieldAndTextCreate("IP",clientContainer,1,tk.TOP)
        ip.pack()
        port = self.fieldAndTextCreate("Port",clientContainer,1,tk.TOP)
        port.pack()
        self.buttomCreate("Join",clientContainer,lambda: controller.show_frame(clientConnectedScreen))
        

class clientConnectedScreen(BaseScreen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        clientContainer = self.containerCreate()
        self.fieldAndTextCreate("Você se conectou ao servidor!",clientContainer)
        self.buttomCreate("Disconnect",clientContainer,lambda: controller.show_frame(MainScreen))

class serverCreatedScreen(BaseScreen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        clientContainer = self.containerCreate()
        self.fieldAndTextCreate("Você criou o servidor",clientContainer)
        self.portaServer = tk.Label(clientContainer, text=f"Port:", font=self.fontePadrao)
        self.portaServer.pack(side=tk.TOP)
        self.buttomCreate("Close Server",clientContainer,lambda: controller.show_frame(MainScreen))    

root = tk.Tk()
app = Application(root)
root.geometry("640x360")
root.title("QuickClip")
root.mainloop()