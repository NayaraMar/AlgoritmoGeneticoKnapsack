from tsp import calcular_distancia_rota, rota_eh_valida, calcular_fitness, CIDADES

rotas_teste = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],        # válida
    [0, 9, 8, 4, 10, 2, 1, 3, 12, 7, 11, 6, 5],        # válida
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0],         # inválida (0 repetida)
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],            # inválida (faltando cidade)
    [0, 2, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 11]         # inválida (cidades repetidas)
]

for idx, rota in enumerate(rotas_teste, start=1):
    print(f"Rota {idx}: {rota}")
    
    valida = rota_eh_valida(rota)  # <-- passa a rota individual
    print(f"É válida? {'Sim' if valida else 'Não'}")
    
    if valida:
        distancia = calcular_distancia_rota(rota)
        fitness = calcular_fitness(rota)
        print(f"Distância total: {distancia:.2f} milhas")
        print(f"Fitness: {fitness:.8f}")
    else:
        print("Distância total: N/A")
        print("Fitness: N/A")
    
    print("-" * 50)