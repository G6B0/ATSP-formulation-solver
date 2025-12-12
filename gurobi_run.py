from experimentación_gurobi import correr_experimentos

def main():
    print("=== EJECUTANDO EXPERIMENTOS ATSP CON GUROBI ===\n")

    input_folder = "data/"
    output_csv = "resultados_gurobi.csv"
    time_limit = 3600

    correr_experimentos(
        input_folder=input_folder,
        output_csv=output_csv,
        time_limit=time_limit
    )

    print("\n=== EXPERIMENTOS COMPLETADOS ===")

if __name__ == "__main__":
    main()
