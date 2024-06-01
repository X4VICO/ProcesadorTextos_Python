from tkinter import * # libreria de tkinter para mostrar el editor
from tkinter import messagebox # dentro de tkinter, llamo a la librería que mostrará ventanas con mensajes
from tkinter import filedialog as tkfile # dentro de tkinter, llamo a la librería que me permite abrir ventanas de dialogo, para escoger archivos en el sistema
import os # libreria para interactuar con el sistema operativo y así tener un mayor manejo de los PATH

# --------------------------config. ventana TKINTER--------------------------
# ---también definiré variables que usaré mas adelante---
root = Tk()
titulo = ": Procesador de textos | By xavico"
ubi_archivo = "Sin título"
texto_inicial = ""
guardado = ""
root.title(guardado + ubi_archivo + titulo)
linea = 1
columna = 0

# --------------------------funciones--------------------------
# usaré global para poder usar los valores de las variables que se utilizan fuera de las funciones
 
# ---función para guardar el texto inicial que hay en el procesador de texto---
def inicio_texto():
    global texto_inicial
    texto_inicial = caja_texto.get("1.0", "end-1c") # en caja_texto guardaré desde la primera posición de texto hasta el final 

# ---función para comprobar si han habido modificaciones en el procesador de texto---
def modificacion_teclado(event): # cada vez que se use el teclado, se hará una comparación con el texto inicial con el actual
    global guardado, texto_inicial
    texto_actual = caja_texto.get("1.0", "end-1c")
    if texto_actual != texto_inicial: # si no coincide, muestro un asterisco para que el usuario sepa  que hay cambios en el archivo respecto al inicial
        guardado = "*"
    else:
        guardado = "" 
    root.title(guardado + os.path.basename(ubi_archivo) + titulo) # actualizo el estado de "guardado" en el titulo de la ventana

    # ---contador de línea y columna---
    # para saber en que posición se encuentra un carácter 
    linea, columna = map(int, caja_texto.index("insert").split(".")) # (como es un añadido he usado ChatGPT de refuerzo en esta línea)
    contador.set(f"Línea: {linea}, Columna: {columna}") # actualizo el estado de "contador"


# --------------------------funciones de menú ARCHIVO--------------------------
# "event=None" es para poder hacer uso de atajos de teclado

# ---función para nuevo archivo---
def nuevo_archivo(event=None): 
    # en el caso de que se vaya a crear un archivo nuevo y se encuentren diferencias del texto actual con el inicial, se avisará al usuario
    global ubi_archivo, guardado
    if guardado == "*": # declaro la condición
        respuesta = messagebox.askyesno("Procesador de textos | By Xavi Conde", "Hay cambios no guardados en " + os.path.basename(ubi_archivo) + "\n¿Te da igual perderlo?") # aviso al usuario
        if respuesta: # salta mensaje de aviso con opción de "sí" o "no". En el caso de "si", cambio estado de guardado y vuelvo a ejecutar la función
            guardado = ""
            root.title(guardado + os.path.basename(ubi_archivo) + titulo)
            nuevo_archivo()
    else: # al ser un archcivo nuevo, elimino el contenido de la caja de texto y actaulizo el titulo del archivo
        caja_texto.delete("1.0", "end")
        ubi_archivo = "Sin título"
        inicio_texto()
        root.title(guardado + ubi_archivo + titulo)

# ---función para abrir archivo---   
def abrir_archivo(event=None):
    # para la función abrir archivo, la primera parte es parecida a la lógica de "nuevo_archivo"
    global ubi_archivo, guardado
    if guardado == "*":
        respuesta = messagebox.askyesno("Procesador de textos | By Xavi Conde", "Hay cambios no guardados en " + os.path.basename(ubi_archivo) + "\n¿Te da igual perderlo?")
        if respuesta:
            try:
                guardado = ""
                abrir_archivo()
            except FileNotFoundError:
                return
    else: # utilizo "try" ya que si se cancela la búsqueda en el explorador de archivos, no modifique el valor de las variables
        try:
            ubi_archivo_Nuevo = tkfile.askopenfilename(initialdir = '.', filetype = (("Archivos de texto", "*.txt"),), title = "Abrir archivo") # ventana de explorador de archivos
            archivo = open(ubi_archivo_Nuevo, 'r') # abro el archivo selecionado en modo lectura
            contenido = archivo.read() # paso el contenido del archivo a una variable nueva
            archivo.close() # cierro el archivo
            caja_texto.delete("1.0", "end") # dejo en blanco la caja de texto
            caja_texto.insert('insert', contenido) # paso el contenido del texto que se quiere abrir a la caja de texto
            inicio_texto() # guardo texto actual
            guardado = "" # actualizo estado
            ubi_archivo = ubi_archivo_Nuevo
            root.title(guardado + os.path.basename(ubi_archivo) + titulo) # actualizo titulo de la ventana
        except FileNotFoundError:
            return

# ---función para guardar archivo---   
def guardar_archivo(event=None): 
    global ubi_archivo, guardado
    if guardado == "*": # esta función solo se activa si se cumple la condición de tener alguna modificación
        if ubi_archivo != "Sin título": # en el caso de que se quiera guardar un archivo nuevo, se utilice la función "guardar _archivo_como"
            contenido = caja_texto.get("1.0", "end-1c") # seleciono el contenido que hay en la caja de texto
            archivo = open(ubi_archivo, 'w+') # abro el archivo en modo escritura
            archivo.write(contenido) # paso el contenido de la caja de texto al archivo
            archivo.close()
            inicio_texto() # guardo texto actual
            guardado ="" # actualizo estado
            root.title(guardado + os.path.basename(ubi_archivo) + titulo) # actualizo titulo de la ventana
        else:
            guardar_archivo_como() # en el caso de que el archivo que se va a guardar sea un archivo nuevo, se ejecutará "guardar_archivo_como"

# ---función para guardar archivo nuevo---   
def guardar_archivo_como(event=None):
    global ubi_archivo, guardado
    archivo = tkfile.asksaveasfile(mode = "w", filetype = (("Archivos de texto", "*.txt"),), defaultextension = ".txt",title = "Guardar archivo como...") # ventana de explorador de archivos
    if archivo is not None:
        ubi_archivo = archivo.name # cojo solo el nombre del archivo
        contenido = caja_texto.get("1.0", "end-1c")
        archivo = open(ubi_archivo, 'w+')
        archivo.write(contenido)
        archivo.close()
        inicio_texto()
        guardado = ""
        root.title(guardado + os.path.basename(ubi_archivo) + titulo)

# ---en el caso de que se vaya a cerrar el procesador de texto---
def cerrar_ventana():
    # me aseguro de que antes de que se cierre el procesador de texto el usuario sea consciente de que puede perder cambios no guardados
    if guardado == "*":
        respuesta = messagebox.askyesno("Procesador de textos | By Xavi Conde", "Hay cambios no guardados en " + os.path.basename(ubi_archivo) + "\n¿Te da igual perderlo?")
        if respuesta:
            root.quit()
    else:
        root.quit()

# --------------------------funciones de menú FORMATO--------------------------
# para palicar los formatos, hago uso de las etiquetas
# según la etiqueta que esté aplicada en el texto, se aplicará un formato que defino más adelante

# ---función para asignar formato negrita---
def negrita():
    # utilizo "try" para asegurar de que hay algún texto seleccinado para poder utilizar la función
    try:
        if "negrita" in caja_texto.tag_names("sel.first"): # en el caso de que ya esté la etiqueta aplicada, se elimina para quitar el formato
            caja_texto.tag_remove("negrita", "sel.first", "sel.last")
        else:
            caja_texto.tag_add("negrita", "sel.first", "sel.last") # de no ser así se aplica la etiqueta "negrita"
    except TclError:
        pass

# ---función para asignar formato cursiva---
def cursiva():
    try:
        if "cursiva" in caja_texto.tag_names("sel.first"):
            caja_texto.tag_remove("cursiva", "sel.first", "sel.last")
        else:
            caja_texto.tag_add("cursiva", "sel.first", "sel.last")
    except TclError:
        pass

# ---función para asignar formato subrayado---
def subrayado():
    try:
        if "subrayado" in caja_texto.tag_names("sel.first"):
            caja_texto.tag_remove("subrayado", "sel.first", "sel.last")
        else:
            caja_texto.tag_add("subrayado", "sel.first", "sel.last")
    except TclError:
        pass

# --------------------------menú--------------------------
btn_menu = Menu(root)

# ---botones de menú ARCHIVO que llaman a la función---
# genero "botones" a las que aplico comandos
archivo_menu = Menu(btn_menu, tearoff=0)
archivo_menu.add_command(label = "Nuevo     Ctrl+N", command = nuevo_archivo)
archivo_menu.add_command(label = "Abrir...     Ctrl+A", command = abrir_archivo)
archivo_menu.add_separator()
archivo_menu.add_command(label = "Guardar     Ctrl+S", command = guardar_archivo)
archivo_menu.add_command(label = "Guardar como...     Ctrl+Mayús+S", command = guardar_archivo_como)
archivo_menu.add_separator()
archivo_menu.add_command(label = "Salir", command = cerrar_ventana)
btn_menu.add_cascade(menu = archivo_menu, label = "Archivo") # todos los "botones" que llaman a las funciones están guardados en un desplegable

# ---botones de menú FORMATO que llaman a la función---
# no oculto los botones de formato para que sea más accesible
btn_menu.add_separator()
btn_menu.add_command(label = "Negrita", command = negrita)
btn_menu.add_command(label = "Cursiva", command = cursiva)
btn_menu.add_command(label = "Subrayado", command = subrayado)

# --------------------------caja de texto--------------------------
# ---configuro parametros que tendrá la caja donde podremos escribir---
caja_texto = Text(root)
caja_texto.pack(fill = "both", expand = 1)
caja_texto.config(padx = 10, pady = 10, font = ("Helvetica", 12)) # formato que tendrá el texto
inicio_texto() # guardo el texto con el que se abre la aplicación por primera vez

caja_texto.bind("<KeyRelease>", modificacion_teclado) # asigno la función de "modificacion_teclado" cada vez que se detecte una acción de teclado

# ---configuro el formato que tendrán los tags---
# siempre que un carácter tenga un tag, se aplican los siguientes formatos
caja_texto.tag_configure("negrita", font=(caja_texto.cget("font"), 12, "bold")) 
caja_texto.tag_configure("cursiva", font=(caja_texto.cget("font"), 12, "italic"))
caja_texto.tag_configure("subrayado", underline = True)

# ---contador de columna y línea de la parte inferior---
contador = StringVar()
contador.set(f"Línea: {linea}, Columna: {columna}") # se actualiza la información en la función "modificacion_teclado"
mostrar_contador = Label(root, textvar = contador, padx = 8)
mostrar_contador.pack(side = "right")

# --------------------------atajos de teclado--------------------------
# ---creo atajos de teclado para 3 funciones que considero que serán las más usadas---
root.bind("<Control-s>", guardar_archivo)
root.bind("<Control-S>", guardar_archivo_como) # para guardar como pongo s mayuscula
root.bind("<Control-n>", nuevo_archivo)
root.bind("<Control-a>", abrir_archivo)

# --------------------------iniciar ventana--------------------------
root.protocol("WM_DELETE_WINDOW", cerrar_ventana) # añado un protocolo para que avise al usuario si se va a cerrar la aplicación sin guardar cambios
root.config(menu = btn_menu)
root.mainloop()
