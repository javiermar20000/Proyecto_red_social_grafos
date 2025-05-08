# Agregar despues un arbol de expansion minima
# Importamos la librería NetworkX para trabajar con grafos
import networkx as nx

# Importamos pyplot de matplotlib para visualizar el grafo
import matplotlib.pyplot as plt

# 1. Crear el grafo como no dirigido
G = nx.Graph()  # Creamos un objeto de tipo grafo no dirigido

# 2. Agregar vértices y aristas según las relaciones de amistad
amistades = {
    'Ana': ['Benjamín', 'Carla'],  # Ana es amiga de Benjamín y Carla
    'Benjamín': ['Diego'],         # Benjamín es amigo de Diego
    'Carla': ['Eva']               # Carla es amiga de Eva
}

# Recorremos el diccionario de amistades para agregar las aristas al grafo
for persona, amigos in amistades.items():
    for amigo in amigos:
        G.add_edge(persona, amigo)  # Agregamos una arista entre la persona y cada uno de sus amigos

# 3. Mostrar el grafo completo
plt.figure(figsize=(8, 6))  # Definimos el tamaño de la figura para visualizar el grafo
pos = nx.spring_layout(G)  # Usamos un layout que posiciona los nodos de forma estética
nx.draw(
    G, pos, with_labels=True,         # Dibujamos el grafo con etiquetas en los nodos
    node_color='lightblue',           # Color de los nodos
    node_size=2000,                   # Tamaño de los nodos
    font_size=12,                     # Tamaño de la fuente de las etiquetas
    edge_color='gray'                 # Color de las aristas
)
plt.title("Relaciones de amistad")  # Título del gráfico
plt.show()  # Mostramos el grafo en pantalla

# 4. Función para verificar si dos personas son amigas directas
def son_amigos(persona1, persona2):
    return G.has_edge(persona1, persona2)  # Retorna True si hay una arista entre persona1 y persona2

# Ejemplos de uso de la función para verificar amistades
print("¿Ana y Carla son amigas?", son_amigos("Ana", "Carla"))  # True, porque hay una arista directa
print("¿Ana y Eva son amigas?", son_amigos("Ana", "Eva"))      # False, no hay conexión directa entre Ana y Eva