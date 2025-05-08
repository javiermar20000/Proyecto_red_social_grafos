def mochila_fraccional(pesos, valores, capacidad):
    n = len(pesos)
    vpw = [(valores[i]/pesos[i], pesos[i], valores[i]) for i in range(n)]
    vpw.sort(reverse=True)  # Ordenar por valor/peso

    total_valor = 0.0
    for ratio, peso, valor in vpw:
        if capacidad == 0:
            break
        if peso <= capacidad:
            capacidad -= peso
            total_valor += valor
        else:
            fraccion = capacidad / peso
            total_valor += valor * fraccion
            capacidad = 0

    return total_valor

# Entrada del usuario
pesos = list(map(float, input("Ingresa los pesos separados por coma: ").split(',')))
valores = list(map(float, input("Ingresa los valores separados por coma: ").split(',')))
capacidad = float(input("Ingresa la capacidad total: "))

resultado = mochila_fraccional(pesos, valores, capacidad)
print(f"Valor máximo que se puede obtener: {resultado:.2f}")