import random
from knapsack import knapsack
from individuo import Individuo

class AG:
    def __init__(self, pop_size, dim):
        self.pop_size = pop_size
        self.dim = dim
        self.pop = []
        #criar cada individuo e appendar na população
        for _ in range(self.pop_size):
            genes = [random.randint(0, 1) for _ in range(self.dim)]
            ind = Individuo(genes)
            self.pop.append(ind)

    def avalia_populacao(self):
        for ind in self.pop:
            ganho = knapsack(ind.genes, self.dim)
            ind.fitness = ganho

    #Define quantos e quais competidores participarão do torneio
    def selecao_torneio(self, tamanho_torneio):
        competidores = random.sample(self.pop, tamanho_torneio)
        #Define qual tem o maior fitness entre os escolhidos
        vencedor = max(competidores, key=lambda ind: ind.fitness)
        return vencedor

    #Define um ponto de corte e separa uma parte de cada pai
    def crossover_um_ponto(self, pai1, pai2):
        ponto_corte = random.randint(1, self.dim - 1)
        genes_filho1 = pai1.genes[:ponto_corte] + pai2.genes[ponto_corte:]
        genes_filho2 = pai2.genes[:ponto_corte] + pai1.genes[ponto_corte:]
        return Individuo(genes_filho1), Individuo(genes_filho2)


    def crossover_dois_pontos(self, pai1, pai2):
        #garante que os pontos não sejam iguais e que tenha espaço para os dois
        p1 = random.randint(1, self.dim - 2)
        p2 = random.randint(p1 + 1, self.dim - 1)
        genes_filho1 = pai1.genes[:p1] + pai2.genes[p1:p2] + pai1.genes[p2:]
        genes_filho2 = pai2.genes[:p1] + pai1.genes[p1:p2] + pai2.genes[p2:]
        return Individuo(genes_filho1), Individuo(genes_filho2)

    #decide de forma aleatoria qual pai vai contribuir com cada gene do filho
    def crossover_uniforme(self, pai1, pai2):
        genes_filho1 = []
        genes_filho2 = []
        for i in range(self.dim):
            if random.random() < 0.5:
                genes_filho1.append(pai1.genes[i])
                genes_filho2.append(pai2.genes[i])
            else:
                genes_filho1.append(pai2.genes[i])
                genes_filho2.append(pai1.genes[i])
        return Individuo(genes_filho1), Individuo(genes_filho2)

    #gera novos genes atraves da taxa de mutação
    def mutacao(self, individuo, taxa_mutacao):
        for i in range(len(individuo.genes)):
            if random.random() < taxa_mutacao:
                individuo.genes[i] = 1 - individuo.genes[i]
        return individuo

    def get_melhores(self, n):
        pop_ordenada = sorted(self.pop, key=lambda ind: ind.fitness, reverse=True)
        return pop_ordenada[:n]

    # --- Método principal da Geração ---
    def proxima_geracao(self, tipo_crossover, taxa_crossover, taxa_mutacao, tamanho_torneio, n_elitismo):
        nova_populacao = []
        melhores = self.get_melhores(n_elitismo)
        nova_populacao.extend(melhores)

        while len(nova_populacao) < self.pop_size:
            pai1 = self.selecao_torneio(tamanho_torneio)
            pai2 = self.selecao_torneio(tamanho_torneio)

            filho1, filho2 = None, None
            if random.random() < taxa_crossover:
                if tipo_crossover == 'um_ponto':
                    filho1, filho2 = self.crossover_um_ponto(pai1, pai2)
                elif tipo_crossover == 'dois_pontos':
                    filho1, filho2 = self.crossover_dois_pontos(pai1, pai2)
                elif tipo_crossover == 'uniforme':
                    filho1, filho2 = self.crossover_uniforme(pai1, pai2)
            else:
                filho1, filho2 = Individuo(pai1.genes[:]), Individuo(pai2.genes[:])

            self.mutacao(filho1, taxa_mutacao)
            self.mutacao(filho2, taxa_mutacao)

            nova_populacao.append(filho1)
            if len(nova_populacao) < self.pop_size:
                nova_populacao.append(filho2)
        
        self.pop = nova_populacao


