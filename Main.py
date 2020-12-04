from tkinter import *
import Vista

def main():
    # ----------------- CARGAR EL FRAME ------------------
    root = Tk()
    root.title('Administrador de contactos')
    root.configure(bg = "#53CDB8")
    root.geometry("+350+80")
    root.resizable(0,0)
    Vista.App(root)
    root.mainloop()

if __name__ == "__main__":
    main()