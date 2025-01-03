import tkinter as tk
from tkinter import ttk, messagebox


class CreateUsersWindow:
    
    def __init__(self, parent):
        self.parent = parent
        self.ventana = tk.Toplevel()
        self.configurar_ventana()
        self.crear_widgets()
        
    def configurar_ventana(self):
        self.ventana.title("Crear Usuario")
        self.ventana.geometry("500x300")
        
    def crear_widgets(self):
        frame_campos_entrada = ttk.Frame(self.ventana)
        frame_campos_entrada.pack(pady=15, padx=15, anchor="center")
        
        self.crear_campos_entrada(frame_campos_entrada)
        
        frame_boton = ttk.Frame(self.ventana)
        frame_boton.pack(pady=15, padx=15)
        
        self.crear_botones(frame_boton)
        
    def crear_campos_entrada(self, frame):
        campos = ["username", "contraseña","clave admin"]
        
        self.entries = {}
        
        for i, campo in enumerate(campos):
            tk.Label(frame, text=campo.capitalize()).grid(row=i, column=0, pady=5)
            entry = tk.Entry(frame)
            entry.grid(row=i, column=1, pady=5)
            self.entries[campo] = entry
        
        tk.Label(frame, text="Rol de usuario:").grid(row=3, column=0, pady=5)   
        rol = ttk.Combobox(frame, values=("vendedor", "admin"))
        rol.grid(row=3, column=1, pady=5)
        self.entries["rol"] = rol
        
    def crear_botones(self, frame):
        boton_crear_usuario = tk.Button(frame, text="Crear Usuario", command=self.crear_usuario)
        boton_crear_usuario.pack(pady=5)
        
    def crear_usuario(self):
        valores = {
            "username": self.entries["username"].get(),
            "contrasena": self.entries["contraseña"].get(),
            "rol": self.entries["rol"].get(),
            "clave_admin": self.entries["clave admin"].get(),
        }
        
        exito, mensaje = self.parent.usuario_controller.crear_usuario(**valores)
        
        if exito:
            messagebox.showinfo("Exito", mensaje)
            self.ventana.destroy()
        else:
            messagebox.showerror("Error", mensaje)
            
        
