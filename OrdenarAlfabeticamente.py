import csv

# ----------------- LEER ARCHIVO CSV ---------------------------------------------

def ordenAlfabetico():
    orden = []
    fila = []
    with open('lista_contactos.csv', 'r') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            nombre = str(row[0])
            telefono = str(row[1])
            email = str(row[2])
            fila = [nombre, telefono, email]
            orden.append(fila)
    listaOrdenada = ordenamiento_por_mezcla(orden)
    return listaOrdenada


# ----------------- MÉTODO PARA ORDENAR LA LISTA ALFABÉTICAMENTE ---------------------------------------------

def ordenamiento_por_mezcla(lista):
    if len(lista) > 1:
        medio = len(lista) // 2
        izquierda = lista[: medio]
        derecha = lista[medio:]
        # --------------- Recursividad ---------------------------
        ordenamiento_por_mezcla(izquierda)
        ordenamiento_por_mezcla(derecha)
        # --------------- Iteradores para leer las dos sublistas ---------------------
        i = 0
        j = 0
        # --------------- Iterator for read the main list -------------------------
        k = 0
        # --------------- Loop principal de la función -------------------------------
        while i < len(izquierda) and j < len(derecha):
            if izquierda[i] < derecha[j]:
                lista[k] = derecha[j]
                j += 1
            else:
                lista[k] = izquierda[i]
                i += 1
            k += 1
        # --------------- Bucle izquierdo de la función -------------------------------
        while i < len(izquierda):
            lista[k] = izquierda[i]
            i += 1
            k += 1
        # --------------- Bucle izquierdo de la función -------------------------------
        while j < len(derecha):
            lista[k] = derecha[j]
            j += 1
            k += 1
    # --------------- El final de la función retorna la lista ordenada ------------------
    return lista