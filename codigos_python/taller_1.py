import networkx as nx
import matplotlib.pyplot as plt

# Datos simulados
usuarios: set = set()
interacciones: dict = {}  # (usuario1, usuario2) : likes
usuario_actual: str = None

def registrar_usuario() -> None:
    global usuarios
    nombre: str = input("Ingrese nombre de usuario: ").strip()
    if nombre in usuarios:
        print("Ese usuario ya existe.")
    else:
        usuarios.add(nombre)
        print(f"Usuario '{nombre}' registrado con éxito.")

def iniciar_sesion() -> None:
    global usuario_actual
    nombre: str = input("Ingrese su nombre de usuario: ").strip()
    if nombre in usuarios:
        usuario_actual = nombre
        print(f"Has iniciado sesión como '{nombre}'.")
    else:
        print("Ese usuario no existe.")

def cerrar_sesion() -> None:
    global usuario_actual
    if usuario_actual:
        print(f"Sesión cerrada de '{usuario_actual}'.")
        usuario_actual = None
    else:
        print("No hay sesión activa.")

def dar_like() -> None:
    if not usuario_actual:
        print("Primero debes iniciar sesión.")
        return

    destino: str = input("¿A qué usuario quieres darle like?: ").strip()
    if destino == usuario_actual:
        print("No puedes darte like a ti mismo.")
        return
    if destino not in usuarios:
        print("Ese usuario no existe.")
        return

    par: tuple = tuple(sorted((usuario_actual, destino)))
    interacciones[par] = interacciones.get(par, 0) + 1
    print(f"Le diste like a '{destino}'. Total de likes entre ustedes: {interacciones[par]}")

def mostrar_menu() -> None:
    print("\n--- MENÚ ---")
    print("1. Registrar usuario")
    print("2. Iniciar sesión")
    print("3. Dar like a otro usuario")
    print("4. Cerrar sesión")
    print("5. Salir y mostrar grafo")

def generar_grafo() -> None:
    G = nx.Graph()

    for usuario in usuarios:
        G.add_node(usuario)

    for (u1, u2), peso in interacciones.items():
        G.add_edge(u1, u2, weight=peso)

    pos = nx.spring_layout(G)
    edges = G.edges(data=True)
    weights = [d['weight'] for (u, v, d) in edges]

    nx.draw(G, pos, with_labels=True, node_color='lightgreen', node_size=2000, font_size=12)
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): d['weight'] for u, v, d in edges})
    nx.draw_networkx_edges(G, pos, width=[weight for weight in weights])

    plt.title("Red Social - Interacciones por Likes")
    plt.show()

# Programa principal
while True:
    mostrar_menu()
    opcion = input("Elige una opción: ").strip()
    
    match opcion:
        case "1":
            registrar_usuario()
        case "2":
            iniciar_sesion()
        case "3":
            dar_like()
        case "4":
            cerrar_sesion()
        case "5":
            cerrar_sesion()
            generar_grafo()
            break
        case _:
            print("Opcion no válida")

    