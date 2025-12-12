from experimentacion_cplex import correr_experimentos

def main():
    print("=== EJECUTANDO EXPERIMENTOS ATSP CON CPLEX ===\n")

    input_folder = "data/"
    output_csv = "resultados_cplex.csv"
    time_limit = 3600

    correr_experimentos(
        input_folder=input_folder,
        output_csv=output_csv,
        time_limit=time_limit
    )

    print("\n=== EXPERIMENTOS CPLEX COMPLETADOS ===")

if __name__ == "__main__":
    main()
