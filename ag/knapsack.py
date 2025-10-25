def _knapsack_constants(dim):
    GANHOS = []
    PESOS = []
    CAPACIDADE_MAXIMA = 0
    if dim == 20:
        GANHOS = [92, 4, 43, 83, 84, 68, 92, 82, 6, 44, 32, 18, 56, 83, 25, 96, 70, 48, 14, 58]
        PESOS = [44, 46, 90, 72, 91, 40, 75, 35, 8, 54, 78, 40, 77, 15, 61, 17, 75, 29, 75, 63]
        CAPACIDADE_MAXIMA = 878
    return GANHOS, PESOS, CAPACIDADE_MAXIMA


def knapsack(solution, dim=20):
    GANHOS, PESOS, CAPACIDADE_MAXIMA = _knapsack_constants(dim)
    ganho_total = 0
    peso_total = 0
    for i in range(len(solution)):
        if solution[i] == 1:
            ganho_total += GANHOS[i]
            peso_total += PESOS[i]

    if peso_total > CAPACIDADE_MAXIMA:
        return 0  
    return ganho_total