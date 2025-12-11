import os
import csv
import lectura_atsp as loader

from gurobi_atsp import solve_atsp_mtz, solve_atsp_gg

def correr_experimentos(input_folder="data/", output_csv="resultados_gurobi.csv", time_limit=3600):

    modelos = {
        "MTZ": solve_atsp_mtz,
        "GG": solve_atsp_gg
    }

    # Abrir CSV
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # Escribir encabezados
        writer.writerow([
            "Instancia",
            "Nodos",
            "Modelo",
            "Variables",
            "Restricciones",
            "Tiempo(s)",
            "Gap(%)",
            "Best Bound / Valor Objetivo"
        ])

        # Recorrer archivos ATSP
        for filename in os.listdir(input_folder):
            if filename.endswith(".atsp"):
                path = os.path.join(input_folder, filename)

                print(f"\n>>> Procesando instancia: {filename}")

                C, n = loader.cargar_matrix(path)

                # Ejecutar cada modelo
                for nombre_modelo, funcion in modelos.items():
                    print(f"   - Ejecutando {nombre_modelo}...")

                    res = funcion(n, C, time_limit=time_limit)

                    #Si no hay solución óptima en tiempo → gap 100%
                    gap = res["gap"] * 100 if res["gap"] != 0 else 0

                    if res["objective_value"] is None:
                        objective = "Inf"
                        gap = 100
                    else:
                        objective = res["objective_value"]

                    writer.writerow([
                        filename,
                        n,
                        nombre_modelo,
                        res["vars"],
                        res["constraints"],
                        round(res["tiempo"], 3),
                        round(gap, 2),
                        objective
                    ])

    print(f"\nTabla guardada en {output_csv}")
