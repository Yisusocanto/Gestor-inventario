import tkinter as tk
from tkinter import ttk, messagebox
from src.controllers.usuario_controller import UsuarioController
from src.views.main_window import MainWindow



class LoginWindow:
    """Ventana de Login"""
    def __init__(self):
        self.ventana = tk.Tk()
        self.usuario_controller = UsuarioController()
        self.configurar_ventana()
        self.crear_widgets()
        
    def configurar_ventana(self):
        self.ventana.title("Login")
        self.ventana.geometry("800x600")
        
    def crear_widgets(self):
        frame_campos_entrada = ttk.Frame(self.ventana)
        frame_campos_entrada.pack(pady=15, padx=15, anchor="center")
        
        self.crear_campos_entrada(frame_campos_entrada)
        
        frame_botones = ttk.Frame(self.ventana)
        frame_botones.pack(pady=15, padx=15)
        
        self.crear_botones(frame_botones)
        
    def crear_campos_entrada(self, frame):
        campos = ["username", "contraseña"]
        
        self.entries = {}
        
        for i, campo in enumerate(campos):
            tk.Label(frame, text=campo.capitalize()).grid(row=i, column=0, pady=5)
            entry = tk.Entry(frame)
            entry.grid(row=i, column=1, pady=5)
            self.entries[campo] = entry
        
    def crear_botones(self, frame):
        boton_ingresar = tk.Button(frame, text="Ingresar", command=self.login)
        boton_ingresar.pack(pady=5)
        
        boton_crear_usuario = tk.Button(frame, text="Crear Usuario", command=self.crear_usuario)
        boton_crear_usuario.pack(pady=5)
        
    def login(self):
        username = self.entries["username"].get()
        contrasena = self.entries["contraseña"].get()
        
        exito, mensaje, usuario = self.usuario_controller.login_verificacion(username, contrasena)
        
        if exito:
            messagebox.showinfo("Exito", mensaje)
            app = MainWindow(usuario)
            app.iniciar()
            self.ventana.destroy()
        else:
            messagebox.showerror("Error", mensaje)
            
    def crear_usuario(self):
        from src.views.create_users_window import CreateUsersWindow
        CreateUsersWindow(self)
        
    def iniciar(self):
        """Inicia la aplicacion desde el login"""
        self.ventana.mainloop()