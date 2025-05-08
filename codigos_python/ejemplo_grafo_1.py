import networkx as nx
import matplotlib.pyplot as plt

# Definir el grafo como un diccionario
grafo = {
    'A': ['B', 'C'],
    'B': ['A', 'D'],
    'C': ['A', 'D'],
    'D': ['B', 'C']
}

# Crear el grafo desde diccionario
G = nx.Graph()  # Usa nx.DiGraph() si es dirigido
for nodo, vecinos in grafo.items():
    for vecino in vecinos:
        G.add_edge(nodo, vecino)

# Dibujar el grafo
plt.figure(figsize=(6, 5))
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color='lightblue',
        node_size=2000, font_size=14)
nx.draw_networkx_edge_labels(G, pos)
plt.title("Visualización del Grafo")
plt.show()