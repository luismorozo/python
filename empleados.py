import tkinter as tk
from tkinter import ttk
import validar  # Asegúrate de que este módulo esté bien implementado

class EmpleadoApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Empleado CRUD")
        self.crear_widgets()
        self.id.focus()  # Dar foco al primer campo al inicio

    def crear_widgets(self):
        ttk.Label(self.master, text="Ingresar ID Empleado", font='Consolas 20').pack(anchor='w', padx=20, pady=15)

        self.master.geometry("500x650+500+200")
        # Campo id con validación
        #self.id = ttk.Entry(self.master, font='Consolas 20', width= 6, validate="key")
        self.id = ttk.Entry(self.master, font='Consolas 20',  validate="key")
        self.id['validatecommand'] = (self.master.register(self.maximalong), '%P')
        self.id.pack(pady=5)
        self.id.bind('<Return>', self.enter)  # Manejar Enter en id
        #self.id.bind('<F1>', self.on_id_return) 
        
        ttk.Label(self.master, text="Apellido:", font='Consolas 14').pack(anchor='w', padx=20)
        self.apellido = ttk.Entry(self.master, font='Consolas 20')
        self.apellido.pack(pady=5)
        self.apellido.bind('<Return>', lambda event: self.nombre.focus())  # Ceder foco al siguiente campo

        ttk.Label(self.master, text="Nombre:", font='Consolas 14').pack(anchor='w', padx=20)
        self.nombre = ttk.Entry(self.master, font='Consolas 20')
        self.nombre.pack(pady=5)
        self.nombre.bind('<Return>', lambda event: self.direccion.focus())  # Ceder foco al siguiente campo

        ttk.Label(self.master, text="Dirección:", font='Consolas 14').pack(anchor='w', padx=20)
        self.direccion = ttk.Entry(self.master, font='Consolas 20')
        self.direccion.pack(pady=5)
        self.direccion.bind('<Return>', lambda event: self.telefono.focus())  # Ceder foco al siguiente campo

        ttk.Label(self.master, text="Teléfono:", font='Consolas 14').pack(anchor='w', padx=20)
        self.telefono = ttk.Entry(self.master, font='Consolas 20')
        self.telefono.pack(pady=5)
        self.telefono.bind('<Return>', lambda event: self.correo.focus())  # Ceder foco al siguiente campo

        ttk.Label(self.master, text="Correo:", font='Consolas 14').pack(anchor='w', padx=20)
        self.correo = ttk.Entry(self.master, font='Consolas 20')
        self.correo.pack(pady=5)
        self.correo.bind('<Return>', lambda event: self.sueldo.focus())  # Cambiar foco al botón aceptar
        
        ttk.Label(self.master, text="Sueldo:", font='Consolas 14').pack(anchor='w', padx=20)
        self.sueldo = ttk.Entry(self.master, font='Consolas 20')
        self.sueldo.pack(pady=5)
        self.sueldo.bind('<Return>', lambda event: self.bAceptar.focus())  # Cambiar foco al botón aceptar
        
        

        self.frame_botones = ttk.Frame(self.master)
        self.frame_botones.pack(pady=15)

        self.bAceptar = ttk.Button(self.frame_botones, text='Aceptar', command=self.aceptar)
        self.bAceptar.pack(side=tk.LEFT, padx=10)
        self.bAceptar.bind('<Return>',self.enter_key)
    

        self.bSalir = ttk.Button(self.frame_botones, text='Salir', command=self.salir)
        self.bSalir.pack(side=tk.LEFT, padx=10)
    def bAceptar(self):
        print('dieron enter en aceptar')
        
        
    def enter_key(self,event):        
        if event.widget ==  self.bAceptar:
            self.bAceptar.invoke()
        elif event.widget== self.bSalir:
            self.bSalir.invoke()    
            

    def maximalong(self, new_value):
        """Validar que el valor en id sea numérico y tenga un máximo de 4 dígitos."""
        if new_value == "":
            return True  # Permitir vacío
        if new_value.isdigit() and len(new_value) <= 4:
            return True  # Permitir valores numéricos de hasta 4 dígitos
        return False  # Rechazar cualquier otro valor

    def enter(self, event):
        """Manejo del evento de retorno en el campo id."""
        
        self.funcod()  # Cargar datos del empleado
        #self.limpiar()
        self.apellido.focus()  # Siempre ceder foco al siguiente campo
        

    def funcod(self):
        """Cargar los datos del empleado desde la base de datos."""
        conexion = validar.conectar()
        cursor = conexion.cursor()
        sql = "SELECT * FROM empleados WHERE id = %s"

        cursor.execute(sql, (self.id.get(),))
        registro = cursor.fetchone()

        # Limpiar los campos antes de llenar nuevos datos
        self.limpiar()
        
        #self.apellido.delete(0, tk.END)
        #self.nombre.delete(0, tk.END)
        #self.direccion.delete(0, tk.END)
        ##self.telefono.delete(0, tk.END)
        #self.correo.delete(0, tk.END)
         
        if registro:
            self.apellido.insert(0, registro[5])  # Nombre
            self.nombre.insert(0, registro[1])  # Nombre
            self.direccion.insert(0, registro[2])  # Dirección
            self.telefono.insert(0, registro[4])  # Teléfono
            self.correo.insert(0, registro[3])  # Correo
            self.sueldo.insert(0,str(registro[6]))
        cursor.close()  # Cerrar el cursor
        conexion.close()  # Cerrar la conexión
    
    def limpiar(self):
        self.apellido.delete(0, tk.END)
        self.nombre.delete(0, tk.END)
        self.direccion.delete(0, tk.END)
        self.telefono.delete(0, tk.END)
        self.correo.delete(0, tk.END)
        self.sueldo.delete(0,tk.END)
          
        
    def aceptar(self):
        """Insertar o actualizar empleado en la base de datos."""
        conexion = validar.conectar()
        cursor = conexion.cursor()

        # Verificar si el ID ya existe
        sql = "SELECT * FROM empleados WHERE id = %s"
        cursor.execute(sql, (self.id.get(),))
        registro = cursor.fetchone()

        # Insertar o actualizar según corresponda
        if registro:  # Si existe, actualizar
            sql_update = "UPDATE empleados SET apellido=%s, nombre = %s, direccion = %s, telefono = %s, correo = %s,sueldo = %s WHERE id = %s"
            cursor.execute(sql_update, (self.apellido.get(), self.nombre.get(), self.direccion.get(), self.telefono.get(),
                                        self.correo.get(),self.sueldo.get(), self.id.get()))
        else:  # Si no existe, insertar
            sql_insert = "INSERT INTO empleados (id, apellido,  nombre, direccion, telefono, correo, sueldo) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql_insert, (self.id.get(), self.apellido.get(),self.nombre.get(), self.direccion.get(), self.telefono.get(), self.correo.get(),self.sueldo.get()))
        
        conexion.commit()  # Confirmar cambios
        cursor.close()  # Cerrar el cursor
        conexion.close()  # Cerrar la conexión

        # Limpiar todos los campos después de insertar/actualizar
        self.limpiar()
        #self.apellido.delete(0,tk.END)
        ##self.nombre.delete(0, tk.END)
        #self.direccion.delete(0, tk.END)
        #self.telefono.delete(0, tk.END)
        #self.correo.delete(0, tk.END)
        self.id.delete(0, tk.END)  # Limpiar id también
        self.id.focus()  # Volver a dar foco al primer campo
        
      

    def salir(self):
        """Cerrar la aplicación."""
        self.master.quit()  # Cerrar la aplicación

if __name__ == "__main__":
    root = tk.Tk()
    app = EmpleadoApp(root)
    root.mainloop()