from tkinter import *
from tkinter import ttk
from tkinter import messagebox as MessageBox
import OrdenarAlfabeticamente
import csv

# -------------------------- FUNCIONES GLOBALES ------------------------------------------

# ----------- DIALOGOS ---------------------------------------
def noEncontrado(var):
    var_s = str(var)
    MessageBox.showinfo("No encontrado", var_s + ' ' + "no encontrado")

def escribirNombre():
    MessageBox.showinfo("No encontrado", "Necesitas escribir un contacto")

def escribirContacto():
    MessageBox.showinfo("Escribir un contacto", "Necesitas escribir la información de un contacto para usar la opción de insertar")

def mbxBorrar(nombre):
    var_nombre = str(nombre)
    if var_nombre == '':
        escribirNombre()
    else:
        opcion = MessageBox.askquestion("Confirmar borrado", "¿Quieres eliminar este contacto?\n" + var_nombre)
        if opcion == "yes":
            return True
        else:
            return False

def mbxEditar(contact):
    var_nombre = str(contact[0])
    var_telefono = str(contact[1])
    var_email = str(contact[2])
    opcion = MessageBox.askquestion("Modificar contacto", "¿Quieres aplicar los cambios?\n" + " Nombre:" + var_nombre + "\n Teléfono:" + var_telefono + "\n Email:" + var_email)
    if opcion == "yes":
        return True
    else:
        return False

# -------------------- DECLARACIÓN DE LA GUI EN LA CLASE APP -------------------------------
class App():
    def __init__(self, root):
        self.window = root

        # ------------------ MENU DECLARATION -----------------
        menubar = Menu(self.window)
        self.window.config(menu=menubar)

        filemenu = Menu(menubar, tearoff=0, bg="#FFBB20")
        filemenu.add_command(label="Mostrar contactos", command=lambda: mostrarContactos(),
                             font=("Arial", "9", "normal"))
        filemenu.add_separator()
        filemenu.add_command(label="Cerrar", command=self.window.quit, font=("Arial", "9", "normal"))

        menubar.add_cascade(label="Menu", menu=filemenu)

        # ---------------- DELACRACIÓN FRAMES -----------------
        inbox_frame = LabelFrame(self.window, bg="#53CDB8")
        inbox_frame.grid(row=0, column=0)

        button_frame = LabelFrame(self.window, bg="#53CDB8")
        button_frame.grid(row=2, column=0)

        three_frame = LabelFrame(self.window, bg="#53CDB8")
        three_frame.grid(row=4, column=0)

        three_button_frame = LabelFrame(self.window, bg="#53CDB8")
        three_button_frame.grid(row=5, column=0)

        # --------------- INBOX WIDGETS ZONE ------------------
        Label(inbox_frame, text='Nombre', bg="#53CDB8", font=("Arial", "11", "normal")).grid(row=0, column=0)
        inbox_nombre = Entry(inbox_frame, font=("Arial", "11", "normal"), width=28)
        inbox_nombre.grid(row=1, column=0)
        inbox_nombre.focus()

        Label(inbox_frame, text='Teléfono', bg="#53CDB8", font=("Arial", "11", "normal")).grid(row=0, column=1)
        inbox_telefono = Entry(inbox_frame, font=("Arial", "11", "normal"), width=20)
        inbox_telefono.grid(row=1, column=1)

        Label(inbox_frame, text='Email', bg="#53CDB8", font=("Arial", "11", "normal")).grid(row=0, column=2)
        inbox_Email = Entry(inbox_frame, font=("Arial", "11", "normal"), width=30)
        inbox_Email.grid(row=1, column=2)

        # --------------- BOTONES -----------------
        btnAnadir = Button(button_frame, command=lambda: anadir(), text='Añadir contacto', width=20)
        btnAnadir.configure(bg="#00FF00", cursor='hand2', font=("Arial", "10", "normal"))
        btnAnadir.grid(row=0, column=0, padx=2, pady=3, sticky=W + E)

        btnBuscar = Button(button_frame, command=lambda: buscar(), text='Buscar contacto', width=20)
        btnBuscar.configure(bg="#808080", cursor='hand2', font=("Arial", "10", "normal"))
        btnBuscar.grid(row=0, column=1, padx=2, pady=3, sticky=W + E)

        btnBorrar = Button(button_frame, command=lambda: borrar(), text='Borrar contacto', width=20)
        btnBorrar.configure(bg="#F26262", cursor='hand2', font=("Arial", "10", "normal"))
        btnBorrar.grid(row=1, column=0, padx=2, pady=3, sticky=W + E)

        btnEditar = Button(button_frame, command=lambda: modificar(), text='Editar contacto')
        btnEditar.configure(bg="#FFBB20", cursor='hand2', font=("Arial", "10", "normal"))
        btnEditar.grid(row=1, column=1, padx=2, pady=3, sticky=W + E)

        btnMostrarContactos = Button(button_frame, command=lambda: mostrarContactos(), text='Mostrar contactos', width=20)
        btnMostrarContactos.configure(bg="#ffffff", cursor='hand2', font=("Arial", "10", "normal"))
        btnMostrarContactos.grid(row=0, column=2, padx=2, pady=3, sticky=W + E)

        btnGuardarCambios = Button(button_frame, command=lambda: limpiar(), text='Limpiar lista', width=20)
        btnGuardarCambios.configure(bg="#ffffff", cursor='hand2', font=("Arial", "10", "normal"))
        btnGuardarCambios.grid(row=1, column=2, padx=2, pady=3, sticky=W + E)

        # -------------- COMBOBOX ----------------
        Label(button_frame, text='Buscar/Modificar selección', bg="#53CDB8", font=("Arial", "10", "normal")).grid(
            row=0, column=3, columnspan=3)

        combo = ttk.Combobox(button_frame, state='readonly', width=17, justify='center',
                             font=("Arial", "10", "normal"))
        combo["values"] = ['Nombre', 'Teléfono', 'Email']
        combo.grid(row=1, column=3, padx=15)
        combo.current(0)

        # --------------- ZONA DEL ÁRBOL DEL DIRECTORIO -----------------
        # Tabla para la base de datos
        self.tree = ttk.Treeview(three_frame, height=20, columns=("one", "two"))
        self.tree.grid(padx=5, pady=5, row=0, column=0, columnspan=1)
        self.tree.heading("#0", text='Nombre', anchor=CENTER)
        self.tree.heading("one", text='Teléfono', anchor=CENTER)
        self.tree.heading("two", text='Email', anchor=CENTER)

        # Scroll
        scrollVert = Scrollbar(three_frame, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollVert.set)
        scrollVert.grid(row=0, column=1, sticky="nsew")

        scroll_x = Scrollbar(three_frame, command=self.tree.xview, orient=HORIZONTAL)
        self.tree.configure(xscrollcommand=scroll_x.set)
        scroll_x.grid(row=2, column=0, columnspan=1, sticky="nsew")

        # -------------------------- DECLARACIÓN FUNCIONES LLAMADAS POR BOTONES -----------------------------

        # --------------- FUNCIONES AUXILIARES ------------------
        def _clean_inbox():
            # Borrar desde primera posición (0) hasta la última posición ('end')
            inbox_nombre.delete(0, 'end')
            inbox_telefono.delete(0, 'end')
            inbox_Email.delete(0, 'end')

        def _clean_treeview():
            tree_list = self.tree.get_children()
            for item in tree_list:
                self.tree.delete(item)

        def _view_csv():
            contactos = OrdenarAlfabeticamente.ordenAlfabetico()
            for i, row in enumerate(contactos):
                nombre = str(row[0])
                telefono = str(row[1])
                email = str(row[2])
                self.tree.insert("", 0, text=nombre, values=(telefono, email))

        def _guardar(nombre, telefono, email):
            s_nombre = nombre
            s_telefono = telefono
            s_email = email
            with open('lista_contactos.csv', 'a') as f:
                writer = csv.writer(f, lineterminator='\r', delimiter=',')
                writer.writerow((s_nombre, s_telefono, s_email))

        def _buscar(var_inbox, posicion):
            list = []
            s_var_inbox = str(var_inbox)
            var_posicion = int(posicion)
            with open('lista_contactos.csv', 'r') as f:
                reader = csv.reader(f)
                for i, row in enumerate(reader):
                    if s_var_inbox == row[var_posicion]:
                        list = [row[0], row[1], row[2]]
                        break
                    else:
                        continue
            return list

        def _check(respuesta, var_buscar):
            listaRespuestas = respuesta
            var_buscar = var_buscar
            if listaRespuestas == []:
                noEncontrado(var_buscar)
            else:
                nombre = str(listaRespuestas[0])
                telefono = str(listaRespuestas[1])
                email = str(listaRespuestas[2])
                self.tree.insert("", 0, text="------------------------------",
                                 values=("------------------------------", "------------------------------"))
                self.tree.insert("", 0, text=nombre, values=(telefono, email))
                self.tree.insert("", 0, text="Buscar resultado de nombre",
                                 values=("Buscar resultado de teléfono", "Buscar resultado de email"))
                self.tree.insert("", 0, text="------------------------------",
                                 values=("------------------------------", "------------------------------"))

        def _check_1(answer, var_search):
            val_modify = answer
            var = var_search
            if val_modify == []:
                noEncontrado(var)
            else:
                VentanaSuperiorModificar(self.window, val_modify)

        # ----------------- BUTTON FUNCTIONS ------------------
        def anadir():
            nombre = inbox_nombre.get()
            telefono = inbox_telefono.get()
            email = inbox_Email.get()
            contact_check = [nombre, telefono, email]
            if contact_check == ['', '', '']:
                escribirContacto()
            else:
                if nombre == '':
                    nombre = '<Default>'
                if telefono == '':
                    telefono = '<Default>'
                if email == '':
                    email = '<Default>'
                _guardar(nombre, telefono, email)
                self.tree.insert("", 0, text="------------------------------",
                                 values=("------------------------------", "------------------------------"))
                self.tree.insert("", 0, text=str(nombre), values=(str(telefono), str(email)))
                self.tree.insert("", 0, text="Nuevo nombre añadido", values=("Nuevo teléfono añadido", "Nueo email añadido"))
                self.tree.insert("", 0, text="------------------------------",
                                 values=("------------------------------", "------------------------------"))
            contact_check = []
            _clean_inbox()

        def buscar():
            respuesta = []
            var_buscar = str(combo.get())
            if var_buscar == 'Nombre':
                var_inbox = inbox_nombre.get()
                posicion = 0
                respuesta = _buscar(var_inbox, posicion)
                _check(respuesta, var_buscar)
            elif var_buscar == 'Teléfono':
                var_inbox = inbox_telefono.get()
                posicion = 1
                respuesta = _buscar(var_inbox, posicion)
                _check(respuesta, var_buscar)
            else:
                var_inbox = inbox_Email.get()
                posicion = 2
                respuesta = _buscar(var_inbox, posicion)
                _check(respuesta, var_buscar)
            _clean_inbox()

        def modificar():
            respuesta = []
            var_buscar = str(combo.get())
            if var_buscar == 'Nombre':
                var_inbox = inbox_nombre.get()
                posicion = 0
                respuesta = _buscar(var_inbox, posicion)
                _check_1(respuesta, var_buscar)
            elif var_buscar == 'Teléfono':
                var_inbox = inbox_telefono.get()
                posicion = 1
                respuesta = _buscar(var_inbox, posicion)
                _check_1(respuesta, var_buscar)
            else:
                var_inbox = inbox_Email.get()
                posicion = 2
                respuesta = _buscar(var_inbox, posicion)
                _check_1(respuesta, var_buscar)
            _clean_inbox()

        def mostrarContactos():
            self.tree.insert("", 0, text="------------------------------",
                             values=("------------------------------", "------------------------------"))
            _view_csv()
            self.tree.insert("", 0, text="------------------------------",
                             values=("------------------------------", "------------------------------"))

        def borrar():
            nombre = str(inbox_nombre.get())
            a = mbxBorrar(nombre)
            if a == True:
                with open('lista_contactos.csv', 'r') as f:
                    reader = list(csv.reader(f))
                with open('lista_contactos.csv', 'w') as f:
                    writer = csv.writer(f, lineterminator='\r', delimiter=',')
                    for i, row in enumerate(reader):
                        if nombre != row[0]:
                            writer.writerow(row)
            limpiar()
            mostrarContactos()

        def limpiar():
            _clean_inbox()
            _clean_treeview()

# ------------------------- VENTANA SUPERIOR ----------------------------------------------

class VentanaSuperiorModificar():
    def __init__(self, raiz, val_modify):
        self.raiz_ventana = raiz
        self.val_modificar = val_modify
        self.nombre = str(self.val_modificar[0])
        self.telefono = str(self.val_modificar[1])
        self.email = str(self.val_modificar[2])

        ventana_modificar = Toplevel(self.raiz_ventana)
        ventana_modificar.title("Modificar contacto")
        ventana_modificar.configure(bg="#53CDB8")
        ventana_modificar.geometry("+400+100")
        ventana_modificar.resizable(0, 0)

        # ---------------- DECLARACIÓN MODIFICAR -----------------
        text_frame = LabelFrame(ventana_modificar, bg="#53CDB8")
        text_frame.grid(row=0, column=0)

        button_frame = LabelFrame(ventana_modificar, bg="#53CDB8")
        button_frame.grid(row=2, column=0)

        # --------------- ZONA DE ETIQUETAS DE WIDGETS -----------------
        Label(text_frame, text="¿Seguro que quieres modificar este artículo?", bg="#53CDB8",
              font=("Arial", "11", "normal")).grid(row=0, column=0, columnspan=3)
        Label(text_frame, text=self.nombre, bg="#53CDB8", font=("Arial", "11", "bold")).grid(row=1, column=0)
        Label(text_frame, text=self.telefono, bg="#53CDB8", font=("Arial", "11", "bold")).grid(row=1, column=1)
        Label(text_frame, text=self.email, bg="#53CDB8", font=("Arial", "11", "bold")).grid(row=1, column=2)

        # --------------- INBOX WIDGETS ZONE ------------------
        Label(text_frame, text='Escribe un nuevo nombre', bg="#53CDB8", font=("Arial", "11", "normal")).grid(row=2,
                                                                                                              column=0)
        n_inbox_nombre = Entry(text_frame, font=("Arial", "11", "normal"), width=28)
        n_inbox_nombre.grid(row=3, column=0)
        n_inbox_nombre.focus()

        Label(text_frame, text='Escribe un nuevo teléfono', bg="#53CDB8", font=("Arial", "11", "normal")).grid(row=2,
                                                                                                               column=1)
        n_inbox_telefono = Entry(text_frame, font=("Arial", "11", "normal"), width=20)
        n_inbox_telefono.grid(row=3, column=1)

        Label(text_frame, text='Escribe un nuevo email', bg="#53CDB8", font=("Arial", "11", "normal")).grid(row=2,
                                                                                                               column=2)
        n_inbox_Email = Entry(text_frame, font=("Arial", "11", "normal"), width=30)
        n_inbox_Email.grid(row=3, column=2)

        # --------------- ZONA DE WIDGETS DE BOTONES -----------------
        btnSi = Button(button_frame, command=lambda: si(), text='Sí', width=20)
        btnSi.configure(bg="#F26262", cursor='hand2', font=("Arial", "10", "normal"))
        btnSi.grid(row=1, column=0, padx=2, pady=3, sticky=W + E)

        btnNo = Button(button_frame, command=ventana_modificar.destroy, text='No', width=20, bg="yellow",
                           cursor='hand2')
        btnNo.configure(bg="#FFBB20", cursor='hand2', font=("Arial", "10", "normal"))
        btnNo.grid(row=1, column=1, padx=2, pady=3, sticky=W + E)

        cancel_button = Button(button_frame, command=ventana_modificar.destroy, text='Cancelar', width=20, bg="green",
                               cursor='hand2')
        cancel_button.configure(bg="#FFBB20", cursor='hand2', font=("Arial", "10", "normal"))
        cancel_button.grid(row=1, column=2, padx=2, pady=3, sticky=W + E)

        # ----------------- BUTTON FUNCTIONS ------------------
        def si():
            contact = self.val_modificar
            nuevoNombre = n_inbox_nombre.get()
            nuevoTelefono = n_inbox_telefono.get()
            nuevoEmail = n_inbox_Email.get()
            a = mbxEditar(contact)
            if a == True:
                borrarOld(contact[0])
                anadirNew(nuevoNombre, nuevoTelefono, nuevoEmail)
            ventana_modificar.destroy()

        def anadirNew(nombre, telefono, email):
            s_nombre = nombre
            s_telefono = telefono
            s_email = email
            with open('lista_contactos.csv', 'a') as f:
                writer = csv.writer(f, lineterminator='\r', delimiter=',')
                writer.writerow((s_nombre, s_telefono, s_email))

        def borrarOld(nombreOld):
            nombre = nombreOld
            with open('lista_contactos.csv', 'r') as f:
                reader = list(csv.reader(f))
            with open('lista_contactos.csv', 'w') as f:
                writer = csv.writer(f, lineterminator='\r', delimiter=',')
                for i, row in enumerate(reader):
                    if nombre != row[0]:
                        writer.writerow(row)