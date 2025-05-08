# Agregar despues un arbol de expansion minima
# Importamos la librería NetworkX para manipular grafos
import networkx as nx

# Importamos matplotlib para visualizar el grafo
import matplotlib.pyplot as plt

# 1. Representación del grafo como diccionario de diccionarios
grafo = {
    "Santiago": {"Valparaíso": 100, "Rancagua": 85},  # Santiago tiene rutas hacia Valparaíso (100 km) y Rancagua (85 km)
    "Rancagua": {"Talca": 100},                       # Rancagua tiene una ruta hacia Talca (100 km)
    "Valparaíso": {"La Serena": 400},                 # Valparaíso tiene una ruta hacia La Serena (400 km)
    "Talca": {"Temuco": 300},                         # Talca tiene una ruta hacia Temuco (300 km)
    "La Serena": {},                                  # La Serena no tiene salidas
    "Temuco": {}                                      # Temuco no tiene salidas
}

# Crear el grafo dirigido (las rutas tienen dirección)
G = nx.DiGraph()  # Usamos DiGraph porque las conexiones son unidireccionales

# Agregar nodos y aristas con pesos al grafo
for origen in grafo:
    for destino in grafo[origen]:
        peso = grafo[origen][destino]               # Obtenemos el peso (distancia) de la ruta
        G.add_edge(origen, destino, weight=peso)    # Agregamos la arista al grafo con su peso correspondiente

# Función para mostrar todas las rutas y sus distancias
def mostrar_rutas(grafo):
    print("Rutas y distancias:")  # Título para la salida
    for origen in grafo:
        for destino, distancia in grafo[origen].items():
            print(f"{origen} → {destino}: {distancia} km")  # Mostramos cada ruta con su distancia

# Función para obtener ciudades accesibles directamente desde una ciudad dada
def ciudades_accesibles(origen):
    if origen in grafo:
        return list(grafo[origen].keys())  # Devolvemos una lista con los destinos directos desde la ciudad
    else:
        return []  # Si la ciudad no existe en el grafo, devolvemos una lista vacía

# Mostrar todas las rutas definidas en el grafo
mostrar_rutas(grafo)

# Mostrar las ciudades a las que se puede acceder directamente desde Santiago
print("\nCiudades accesibles desde Santiago:", ciudades_accesibles("Santiago"))

# Dibujar el grafo
pos = nx.spring_layout(G)  # Calculamos posiciones para los nodos de forma visualmente agradable
labels = nx.get_edge_attributes(G, 'weight')  # Obtenemos los pesos de las aristas para mostrarlos como etiquetas

# Dibujamos el grafo con nodos y aristas
nx.draw(
    G, pos, with_labels=True,                 # Mostramos etiquetas en los nodos
    node_color='lightblue',                   # Color de los nodos
    node_size=2000,                           # Tamaño de los nodos
    font_size=10,                             # Tamaño de la fuente
    font_weight='bold',                       # Negrita en los nombres de las ciudades
    arrows=True                               # Mostramos flechas en las aristas para indicar dirección
)

# Dibujamos las etiquetas de las aristas (los pesos/distancias)
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

# Título del gráfico
plt.title("Red de distribución de ciudades")

# Mostrar el grafo en pantalla
plt.show()