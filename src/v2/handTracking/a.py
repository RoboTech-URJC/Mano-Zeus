import tkinter as tk

class MiniInterfaz1:
    def __init__(self, root):
        self.window = root
        self.window.title("Interfaz 1")

        # Agregar widgets a la primera ventana
        self.scale = tk.Scale(self.window, from_=0, to=100, orient=tk.HORIZONTAL)
        self.scale.pack()

        self.button = tk.Button(self.window, text="Obtener valor", command=self.print_val)
        self.button.pack()

    def print_val(self):
        value = self.scale.get()
        print(f"Valor de la escala en Interfaz 1: {value}")

class MiniInterfaz2:
    def __init__(self, root):
        # Crear una ventana secundaria
        self.window = tk.Toplevel(root)
        self.window.title("Interfaz 2")

        # Agregar widgets a la segunda ventana
        self.label = tk.Label(self.window, text="Esta es la Interfaz 2")
        self.label.pack()

        self.button = tk.Button(self.window, text="Cerrar", command=self.window.destroy)
        self.button.pack()

# Crear la ventana principal
root = tk.Tk()

# Inicializar la primera interfaz en la ventana principal
app1 = MiniInterfaz1(root)

# Crear la segunda interfaz como una ventana separada
app2 = MiniInterfaz2(root)

# Ejecutar el bucle principal de Tkinter
root.mainloop()
