import tkinter as tk  # Importa la biblioteca tkinter y le asigna el alias 'tk' para crear interfaces gráficas.
from tkinter import messagebox, filedialog  # Importa módulos específicos de tkinter para mostrar cuadros de mensaje y abrir diálogos de archivos.
from PIL import Image, ImageTk  # Importa clases de la biblioteca PIL (Pillow) para manejar imágenes y convertirlas a un formato que Tkinter pueda usar.
import pymongo  # Importa la biblioteca pymongo para conectarse y trabajar con bases de datos MongoDB.
import networkx as nx  # Importa la biblioteca NetworkX y le asigna el alias 'nx' para crear y manipular grafos/redes.
import matplotlib.pyplot as plt  # Importa matplotlib.pyplot como 'plt' para crear gráficos y visualizaciones (por ejemplo, de grafos).
import os  # Importa el módulo os para interactuar con el sistema operativo (p. ej., rutas de archivos).
from bson import ObjectId  # Importa ObjectId desde bson para trabajar con IDs únicos de documentos en MongoDB.

# Conexión MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")  # Establece conexión con un servidor local de MongoDB.
db = client["red_social"]  # Selecciona o crea la base de datos llamada 'red_social'.
usuarios_col = db["usuarios"]  # Accede a la colección 'usuarios' dentro de la base de datos.
historias_col = db["historias"]  # Accede a la colección 'historias' dentro de la base de datos.

# ------------------- Funciones base -------------------

def registrar_usuario(username, password):  # Define una función para registrar un nuevo usuario.
    if usuarios_col.find_one({"username": username}):  # Verifica si el nombre de usuario ya existe en la colección.
        return False  # Retorna False si el usuario ya está registrado.
    usuarios_col.insert_one({"username": username, "password": password})  # Inserta el nuevo usuario con su contraseña en la base de datos.
    return True  # Retorna True indicando que el registro fue exitoso.

def verificar_credenciales(username, password):  # Define una función para verificar las credenciales de inicio de sesión.
    return usuarios_col.find_one({"username": username, "password": password})  # Busca un usuario con las credenciales dadas; retorna el documento si existe.

def guardar_historia(usuario, texto, imagen_path):  # Define una función para guardar una historia con texto e imagen.
    historias_col.insert_one({  # Inserta un nuevo documento en la colección de historias con los datos proporcionados.
        "usuario": usuario,  # Nombre del autor de la historia.
        "texto": texto,  # Contenido de texto de la historia.
        "imagen": imagen_path,  # Ruta a la imagen asociada.
        "likes": []  # Lista vacía de 'likes' iniciales.
    })

def obtener_historias():  # Define una función para obtener todas las historias almacenadas.
    return list(historias_col.find())  # Retorna todas las historias como una lista de documentos.

def dar_like(historia_id, usuario):  # Define una función para que un usuario pueda dar 'like' a una historia.
    historia = historias_col.find_one({"_id": ObjectId(historia_id)})  # Busca la historia usando su ObjectId.
    if historia and usuario != historia["usuario"] and usuario not in historia["likes"]:  # Verifica que la historia exista, que el usuario no sea el autor y que no haya dado 'like' antes.
        historias_col.update_one({"_id": historia["_id"]}, {"$push": {"likes": usuario}})  # Agrega el usuario a la lista de 'likes' usando $push.

def construir_grafo():  # Define una función llamada 'construir_grafo'
    G = nx.DiGraph()  # Crea un grafo dirigido usando NetworkX
    historias = obtener_historias()  # Llama a una función para obtener las historias (de usuarios)

    for historia in historias:  # Itera sobre cada historia obtenida
        autor = historia['usuario']  # Extrae el autor de la historia
        for liker in historia['likes']:  # Itera sobre cada usuario que le dio "like" a la historia
            if G.has_edge(liker, autor):  # Si ya existe una arista de liker a autor
                G[liker][autor]['weight'] += 1  # Incrementa el peso de la arista en 1
            else:
                G.add_edge(liker, autor, weight=1)  # Si no existe, crea la arista con peso 1

    pos = nx.spring_layout(G, seed=42)  # Genera una disposición de nodos fija (para que sea reproducible)

    edge_labels = {}  # Diccionario para etiquetas de las aristas
    procesados = set()  # Conjunto para registrar aristas ya procesadas y evitar duplicados

    for u, v in G.edges():  # Itera sobre todas las aristas (u: origen, v: destino)
        if (v, u) in procesados:  # Si la arista inversa ya fue procesada
            continue  # Omite esta arista para evitar duplicar la etiqueta

        w1 = G[u][v]['weight']  # Obtiene el peso de la arista de u a v
        w2 = G[v][u]['weight'] if G.has_edge(v, u) else 0  # Obtiene el peso inverso si existe
        total_weight = w1 + w2  # Suma total de interacciones entre ambos nodos

        edge_labels[(u, v)] = f"{total_weight} (<-- {w1}, --> {w2})"  # Crea una etiqueta detallando direcciones
        procesados.add((u, v))  # Marca esta arista como procesada

    plt.figure(figsize=(10, 7))  # Crea una figura de tamaño 10x7
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000,
            arrows=True, arrowstyle='-|>', arrowsize=20)  # Dibuja el grafo con nodos y flechas

    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')  # Dibuja etiquetas de aristas

    plt.title("Interacciones por likes (grafo)")  # Título del gráfico
    plt.show()  # Muestra el gráfico


# ------------------- Interfaz -------------------

class App:  # Define una clase llamada App que representa la aplicación principal.
    def __init__(self, root):  # Método constructor que recibe la ventana principal (root) como parámetro.
        self.root = root  # Guarda la referencia a la ventana principal.
        self.root.title("Red Social con Grafos")  # Establece el título de la ventana.
        self.usuario = None  # Inicializa el atributo de usuario como None (aún no hay sesión iniciada).

        self.login_screen()  # Llama al método que muestra la pantalla de inicio de sesión.

    def login_screen(self):  # Método para construir la pantalla de inicio de sesión.
        for widget in self.root.winfo_children():  # Itera sobre todos los widgets actuales en la ventana...
            widget.destroy()  # ...y los elimina para limpiar la interfaz.

        tk.Label(self.root, text="Usuario").pack()  # Crea y muestra una etiqueta para el campo de usuario.
        self.entry_user = tk.Entry(self.root)  # Crea una entrada de texto para el nombre de usuario.
        self.entry_user.pack()  # Muestra la entrada de texto en la ventana.

        tk.Label(self.root, text="Contraseña").pack()  # Crea y muestra una etiqueta para el campo de contraseña.
        self.entry_pass = tk.Entry(self.root, show="*")  # Crea una entrada de texto para la contraseña, ocultando los caracteres.
        self.entry_pass.pack()  # Muestra la entrada de texto de la contraseña.

        tk.Button(self.root, text="Iniciar sesión", command=self.login).pack()  # Botón que llama al método login al hacer clic.
        tk.Button(self.root, text="Registrarse", command=self.register).pack()  # Botón que llama al método register al hacer clic.

    def register(self):  # Método que maneja el registro de nuevos usuarios.
        user = self.entry_user.get().strip()  # Obtiene el texto ingresado en el campo de usuario y elimina espacios al inicio/final.
        pw = self.entry_pass.get().strip()  # Obtiene el texto ingresado en el campo de contraseña y elimina espacios al inicio/final.
        if not user or not pw:  # Verifica que ambos campos estén completos.
            messagebox.showwarning("Campos vacíos", "Debes completar usuario y contraseña")  # Muestra advertencia si algún campo está vacío.
            return  # Sale del método sin registrar.
        if registrar_usuario(user, pw):  # Intenta registrar al usuario con los datos ingresados.
            messagebox.showinfo("Registro", "Usuario registrado con éxito")  # Muestra mensaje si el registro fue exitoso.
        else:
            messagebox.showwarning("Error", "El usuario ya existe")  # Muestra advertencia si el usuario ya está registrado.

    def login(self):  # Método para iniciar sesión.
        user = self.entry_user.get().strip()  # Obtiene el texto del campo usuario y elimina espacios innecesarios.
        pw = self.entry_pass.get().strip()  # Obtiene el texto del campo contraseña y elimina espacios innecesarios.
        if not user or not pw:  # Verifica si alguno de los campos está vacío.
            messagebox.showwarning("Campos vacíos", "Debes completar usuario y contraseña")  # Muestra advertencia.
            return  # Sale del método.
        if verificar_credenciales(user, pw):  # Verifica si las credenciales son válidas.
            self.usuario = user  # Guarda el nombre de usuario autenticado.
            self.main_screen()  # Llama a la pantalla principal si el login es exitoso.
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")  # Muestra error si las credenciales no son válidas.

    def main_screen(self):  # Método para mostrar la pantalla principal después del login.
        for widget in self.root.winfo_children():  # Elimina todos los widgets actuales de la ventana.
            widget.destroy()

        tk.Label(self.root, text=f"Bienvenido {self.usuario}", font=("Arial", 14)).pack()  # Muestra un saludo personalizado.
        self.texto = tk.Text(self.root, height=4, width=50)  # Crea un campo de texto para escribir la publicación.
        self.texto.pack()  # Muestra el campo de texto.

        self.img_path = None  # Inicializa la ruta de la imagen como None (sin imagen seleccionada).
        tk.Button(self.root, text="Seleccionar imagen", command=self.cargar_imagen).pack()  # Botón para seleccionar imagen.
        tk.Button(self.root, text="Publicar", command=self.publicar).pack()  # Botón para publicar texto e imagen.
        tk.Button(self.root, text="Ver publicaciones", command=self.ver_publicaciones).pack()  # Botón para ver todas las publicaciones.
        tk.Button(self.root, text="Ver grafo", command=construir_grafo).pack()  # Botón para visualizar el grafo de interacciones.
        tk.Button(self.root, text="Cerrar sesión", command=self.login_screen).pack()  # Botón para cerrar sesión y volver a login.

    def cargar_imagen(self):  # Método para cargar una imagen desde el sistema de archivos.
        path = filedialog.askopenfilename(  # Abre un cuadro de diálogo para seleccionar una imagen.
            title="Seleccionar imagen", 
            filetypes=[("Imágenes", "*.png *.jpg *.jpeg")]  # Filtra archivos solo a imágenes comunes.
        )
        if path:  # Si se seleccionó un archivo...
            self.img_path = path  # ...se guarda la ruta del archivo como atributo de la instancia.

    def publicar(self):  # Método para publicar una historia.
        texto = self.texto.get("1.0", tk.END).strip()  # Obtiene el texto completo del campo de texto, eliminando espacios extras.
        if texto:  # Verifica que el texto no esté vacío.
            guardar_historia(self.usuario, texto, self.img_path)  # Guarda la historia con el usuario actual, texto e imagen seleccionada.
            messagebox.showinfo("Publicado", "Tu historia se publicó")  # Muestra mensaje de éxito.
            self.texto.delete("1.0", tk.END)  # Limpia el campo de texto después de publicar.

    def ver_publicaciones(self):  # Método para mostrar todas las publicaciones existentes.
        for widget in self.root.winfo_children():  # Elimina todos los widgets actuales de la ventana.
            widget.destroy()

        historias = obtener_historias()  # Obtiene todas las historias desde la base de datos.
        for historia in historias:  # Recorre cada historia para mostrarla.
            frame = tk.Frame(self.root, borderwidth=2, relief="ridge", padx=10, pady=5)  # Crea un contenedor con borde y espacio.
            frame.pack(pady=5, fill="x")  # Muestra el contenedor en pantalla.

            tk.Label(frame, text=f"{historia['usuario']} dice:", font=("Arial", 10, "bold")).pack(anchor="w")  # Muestra el nombre del autor.
            tk.Label(frame, text=historia["texto"], wraplength=400).pack(anchor="w")  # Muestra el texto de la historia.

            if historia.get("imagen") and os.path.exists(historia["imagen"]):  # Verifica si hay una imagen y si existe en el sistema.
                img = Image.open(historia["imagen"])  # Abre la imagen.
                img.thumbnail((150, 150))  # Redimensiona la imagen a un tamaño pequeño.
                photo = ImageTk.PhotoImage(img)  # Convierte la imagen a un formato que Tkinter puede usar.
                tk.Label(frame, image=photo).pack()  # Muestra la imagen.
                frame.image = photo  # Evita que Python elimine la imagen (referencia persistente).

            likes = historia.get("likes", [])  # Obtiene la lista de usuarios que dieron like.
            like_btn = tk.Button(frame, text=f"👍 {len(likes)} Me gusta",  # Botón para dar like con contador.
                             command=lambda h=historia["_id"]: self.dar_like_y_recargar(h))  # Usa lambda para asociar ID de historia.
            like_btn.pack()  # Muestra el botón de like.

        tk.Button(self.root, text="Volver", command=self.main_screen).pack()  # Botón para regresar a la pantalla principal.

    def dar_like_y_recargar(self, historia_id):  # Método que da like a una historia y recarga la vista.
        dar_like(historia_id, self.usuario)  # Agrega un like desde el usuario actual.
        self.ver_publicaciones()  # Recarga la vista de publicaciones para mostrar el nuevo like.

# ------------------- Ejecutar -------------------

root = tk.Tk()  # Crea la ventana principal de la aplicación.
app = App(root)  # Crea una instancia de la aplicación.
root.mainloop()  # Inicia el bucle principal de la interfaz gráfica.
