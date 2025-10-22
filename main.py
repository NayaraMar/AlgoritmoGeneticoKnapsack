from Ag_knapsack import AG
import time
import numpy as np 
import matplotlib.pyplot as plt 


if __name__ == "__main__":
    DIM = 20
    POP_SIZE = 50
    GERACOES = 500
    TAM_TORNEIO = 3
    TAXA_CROSS = 0.80
    TAXA_MUT = 0.02
    N_ELITE = 2
    N_INSTANCIAS = 30
   
    CONFIGURACOES = ['um_ponto', 'dois_pontos', 'uniforme']

   
    resultados_finais_ag = {}
    historicos_ag = {}        

    print(f"Iniciando Execução")
    tempo_inicio = time.time()

    for config in CONFIGURACOES:
       
        lista_resultados_finais = []
        lista_historicos = []

        for i in range(1, N_INSTANCIAS + 1):
            ag = AG(pop_size=POP_SIZE, dim=DIM)
            ag.avalia_populacao()
           
            melhor_geral = ag.get_melhores(1)[0]
            historico_desta_instancia = []

            for gen in range(GERACOES):
                ag.proxima_geracao(
                    tipo_crossover=config,
                    taxa_crossover=TAXA_CROSS,
                    taxa_mutacao=TAXA_MUT,
                    tamanho_torneio=TAM_TORNEIO,
                    n_elitismo=N_ELITE
                )
                ag.avalia_populacao()
               
                melhor_da_geracao = ag.get_melhores(1)[0]
                if melhor_da_geracao.fitness > melhor_geral.fitness:
                    melhor_geral = melhor_da_geracao
               
                historico_desta_instancia.append(melhor_geral.fitness)
           
            lista_resultados_finais.append(melhor_geral.fitness)
            lista_historicos.append(historico_desta_instancia)

        resultados_finais_ag[config] = lista_resultados_finais
        historicos_ag[config] = lista_historicos

    print(f"\nTempo de execução: {time.time() - tempo_inicio:.2f}s ---")

    print("\n Média e Desvio Padrão (Fitness)")
    melhor_solucao_absoluta_ag = 0
   
    for config in CONFIGURACOES:
        resultados = resultados_finais_ag[config]
        media = np.mean(resultados)
        desvio = np.std(resultados)
        maximo = np.max(resultados)
       
        if maximo > melhor_solucao_absoluta_ag:
            melhor_solucao_absoluta_ag = maximo
           
        print(f"Configuração AG '{config}':")
        print(f"  Média   : {media:.2f}")
        print(f"  Desvio  : {desvio:.2f}")
        print(f"  Máximo  : {maximo}")

    print(f"\nMelhor solução absoluta AG: {melhor_solucao_absoluta_ag}")
   
    dados_hc_tradicional = np.loadtxt("ag/resultados.txt")
    dados_hc_estocastico = np.loadtxt("ag/resultados_estocatisco.txt")
   
    print("\n Resultados Hill Climbing")
    print(f"HC Tradicional: Média {np.mean(dados_hc_tradicional):.2f}, Desvio {np.std(dados_hc_tradicional):.2f}, Máximo {np.max(dados_hc_tradicional)}")
    print(f"HC Estocástico : Média {np.mean(dados_hc_estocastico):.2f}, Desvio {np.std(dados_hc_estocastico):.2f}, Máximo {np.max(dados_hc_estocastico)}")

    plt.figure(figsize=(10, 6))
    for config in CONFIGURACOES:
        matriz_historicos = np.array(historicos_ag[config])
        media_convergencia = np.mean(matriz_historicos, axis=0)
        plt.plot(media_convergencia, label=f'AG Crossover {config}')

    plt.title('Gráfico de Convergência dos AGs')
    plt.xlabel('Geração')
    plt.ylabel('Melhor Fitness (Média)')
    plt.legend()
    plt.grid(True)
    plt.savefig('grafico_convergencia_ag.png')
    print("Salvo como 'grafico_convergencia_ag.png'")
   
    dados_para_boxplot = [
        resultados_finais_ag['um_ponto'],
        resultados_finais_ag['dois_pontos'],
        resultados_finais_ag['uniforme'],
        dados_hc_tradicional,    
        dados_hc_estocastico
    ]
   
    labels = [
        'AG 1-Ponto',
        'AG 2-Pontos',
        'AG Uniforme',
        'HC Tradicional',
        'HC Estocástico'
    ]

    plt.figure(figsize=(12, 7))
    plt.boxplot(dados_para_boxplot, labels=labels, patch_artist=True)
    plt.title('Comparação de Desempenho dos Algoritmos (30 execuções)')
    plt.ylabel('Fitness Final')
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)
    plt.savefig('boxplot_comparativo_final.png') # Salva a imagem
    print("Salvo como 'boxplot_comparativo_final.png'")
   

   
