# Agregar despues un arbol de expansion minima
# Importamos la librería NetworkX para trabajar con grafos
import networkx as nx

# Importamos matplotlib para graficar el grafo
import matplotlib.pyplot as plt

# Importamos numpy para trabajar con matrices
import numpy as np

# Lista de nodos que representan los computadores en la red
nodos = ["PC1", "PC2", "PC3", "PC4", "PC5"]

# Crear un grafo no dirigido (la conexión entre computadores es bidireccional)
G = nx.Graph()

# Agregamos los nodos (computadores) al grafo
G.add_nodes_from(nodos)

# Definimos las conexiones directas entre los computadores
conexiones = [("PC1", "PC2"), ("PC1", "PC3"), ("PC2", "PC4"), ("PC4", "PC5")]

# Agregamos las conexiones como aristas al grafo
G.add_edges_from(conexiones)

# 1. Representamos el grafo como una matriz de adyacencia
# La matriz tendrá un 1 donde hay una conexión directa entre dos nodos y 0 en caso contrario
matriz_adyacencia = nx.to_numpy_array(G, nodelist=nodos, dtype=int)

# 2. Mostramos la matriz completa por consola
print("Matriz de Adyacencia:")
# Imprimimos los nombres de los nodos como encabezado
print("   ", "  ".join(nodos))
# Recorremos cada fila de la matriz y la mostramos junto al nombre del nodo correspondiente
for i, fila in enumerate(matriz_adyacencia):
    print(nodos[i], fila.astype(int))  # Convertimos a entero por claridad (evita decimales innecesarios)

# 3. Definimos una función para verificar si hay conexión directa entre dos computadores
def conexion_directa(pc1, pc2):
    # Obtenemos los índices de los nodos en la lista
    idx1 = nodos.index(pc1)
    idx2 = nodos.index(pc2)
    # Retornamos True si hay un 1 en la matriz (es decir, conexión directa), False si hay un 0
    return matriz_adyacencia[idx1][idx2] == 1

# Ejemplos de uso de la función:
print("\n¿Hay conexión directa entre PC1 y PC3?", conexion_directa("PC1", "PC3"))  # Debería ser True
print("¿Hay conexión directa entre PC1 y PC5?", conexion_directa("PC1", "PC5"))    # Debería ser False

# Visualización del grafo
plt.figure(figsize=(8, 6))               # Definimos el tamaño de la figura
pos = nx.spring_layout(G)                # Calculamos una disposición visual de los nodos
# Dibujamos el grafo con nodos y aristas
nx.draw(G, pos, with_labels=True,        # Mostramos etiquetas (nombres de PCs)
        node_color='lightgreen',         # Color de los nodos
        node_size=2000,                  # Tamaño de los nodos
        font_size=12,                    # Tamaño del texto
        edge_color='black')              # Color de las aristas

# Título del gráfico
plt.title("Conexiones de red local entre computadores")

# Mostramos el gráfico en pantalla
plt.show()