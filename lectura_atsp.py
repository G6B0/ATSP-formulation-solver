def cargar_matrix(path):
    """
    Lee un archivo .atsp con formato:
    EDGE_WEIGHT_TYPE : EXPLICIT
    EDGE_WEIGHT_FORMAT : FULL_MATRIX

    Devuelve:
     C : Matriz NxN (numpy array)
     n : número de nodos (int)
    """

    with open(path, 'r') as f:
        lines = f.readlines()

    n = None
    valor_matrix = []
    lectura_matrix = False

    for line in lines:
        line = line.strip()

        if line.startswith("DIMENSION"):
            n = int(line.split(":")[1].strip())

        if line.startswith("EDGE_WEIGHT_SECTION"):
            lectura_matrix = True
            continue

        if line.startswith("EOF"):
            break

        if lectura_matrix:
            if line == "":
                continue
            valores = [float(x) for x in line.split()]
            valor_matrix.extend(valores)

    if n is None:
        raise ValueError("No se encontró la dimensión en el archivo.")
    
    if len(valor_matrix) != n * n:
        raise ValueError("La cantidad de valores en la matriz no coincide con la dimensión especificada.")
    
    import numpy as np
    C = np.array(valor_matrix).reshape((n, n))

    return C, n