# NOME DO CANDIDATO: Gabriel de Souza Gomes
# CURSO DO CANDIDATO: Engenharia de Computação
# AREAS DE INTERESSE: Visão Computacional e Behavior
# Você pode importar as bibliotecas que julgar necessárias.

import heapq
def encontrar_caminho(pos_inicial, pos_objetivo, obstaculos, largura_grid, altura_grid, tem_bola=False):
    """
    Esta é a função principal que você deve implementar para o desafio EDROM.
    Seu objetivo é criar um algoritmo de pathfinding (como o A*) que encontre o
    caminho ótimo para o robô, considerando os diferentes níveis de complexidade.

    Args:
        pos_inicial (tuple): A posição (x, y) inicial do robô.
        pos_objetivo (tuple): A posição (x, y) do objetivo (bola ou gol).
        obstaculos (list): Uma lista de tuplas (x, y) com as posições dos obstáculos.
        largura_grid (int): A largura do campo em células.
        altura_grid (int): A altura do campo em células.
        tem_bola (bool): Um booleano que indica o estado do robô.
                         True se o robô está com a bola, False caso contrário.
                         Este parâmetro é essencial para o Nível 2 do desafio.

    Returns:
        list: Uma lista de tuplas (x, y) representando o caminho do início ao fim.
              A lista deve começar com o próximo passo após a pos_inicial e terminar
              na pos_objetivo. Se nenhum caminho for encontrado, retorna uma lista vazia.
              Exemplo de retorno: [(1, 2), (1, 3), (2, 3)]

    ---------------------------------------------------------------------------------
    REQUISITOS DO DESAFIO (AVALIADOS EM NÍVEIS):
    ---------------------------------------------------------------------------------
    [NÍVEL BÁSICO: A* Comum com Diagonal]
    O Algoritmo deve chegar até a bola e depois ir até o gol (desviando dos adversários) 
    considerando custos diferentes pdra andar reto (vertical e horizontal) e para andar em diagonal

    [NÍVEL 1: Custo de Rotação]
    O custo de um passo não é apenas a distância. Movimentos que exigem que o robô
    mude de direção devem ser penalizados. Considere diferentes penalidades para:
    - Curvas suaves (ex: reto -> diagonal).
    - Curvas fechadas (ex: horizontal -> vertical).
    - Inversões de marcha (180 graus).

    [NÍVEL 2: Custo por Estado]
    O comportamento do robô deve mudar se ele estiver com a bola. Quando `tem_bola`
    for `True`, as penalidades (especialmente as de rotação do Nível 1) devem ser
    AINDA MAIORES. O robô precisa ser mais "cuidadoso" ao se mover com a bola.

    [NÍVEL 3: Zonas de Perigo]
    As células próximas aos `obstaculos` são consideradas perigosas. Elas não são
    proibidas, mas devem ter um custo adicional para desencorajar o robô de passar
    por elas, a menos que seja estritamente necessário ou muito vantajoso.

    DICA: Um bom algoritmo A* é flexível o suficiente para que os custos de movimento
    (g(n)) possam ser calculados dinamicamente, incorporando todas essas regras.
    """

    # -------------------------------------------------------- #
    #                                                          #
    #             >>>  IMPLEMENTAÇÃO DO CANDIDATO   <<<        #
    #                                                          #
    # -------------------------------------------------------- #

    # O código abaixo é um EXEMPLO SIMPLES de um robô que apenas anda para frente.
    # Ele NÃO desvia de obstáculos e NÃO busca o objetivo.
    # Sua tarefa é substituir esta lógica simples pelo seu algoritmo A* completo.

# ---------------------------------------NIVEL BASICO-----------------------------------------------
    #Variávei Globais
    # Custo para movimentos retos (horizontal ou vertical)
    CUSTO_RETO = 1.0
    # Custo para movimentos diagonais (~sqrt(2))
    CUSTO_DIAGONAL = 1.414 

    # algoritmo A*
    
    # open_set é uma fila de prioridade (usando heapq) que armazena tuplas:
    # (f_score, g_score, (x, y), caminho)
    # f_score: Custo total estimado do caminho (g_score + h_score)
    # g_score: Custo real do início até o nó atual
    # (x, y): Posição atual do nó
    # caminho: Lista de nós que levaram até o nó atual
    open_set = []

    
    # g_score_map armazena o custo real do início até cada nó
    # {node: g_score}
    g_score_map = {pos_inicial: 0}
    
    # h_score_map armazena o custo heurístico (estimado) de cada nó até o objetivo
    # A heurística de distância de Manhattan foi usada, pois o custo computacional é menor
    # para movimentos em grade (mesmo com diagonais, ela não superestima o custo real)
    def heuristica(pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    # Inicializa o A*
    h_inicial = heuristica(pos_inicial, pos_objetivo)
    f_inicial = h_inicial
    heapq.heappush(open_set, (f_inicial, 0, pos_inicial, [])) # (f_score, g_score, nó, caminho_até_nó)

    # Conjunto para armazenar nós já visitados
    closed_set = set()

    while open_set:
        # Pega o nó com o menor f_score
        f_score, g_score, pos_atual, caminho_atual = heapq.heappop(open_set)

        if pos_atual == pos_objetivo:
            # Se o objetivo foi alcançado, retorna o caminho
            return caminho_atual

        if pos_atual in closed_set: #evita que o algoritmo processe o mesmo nó mais de uma vez
            continue
        
        closed_set.add(pos_atual)  #todos os vizinhos do node foram analisados

        # Possíveis movimentos (8 direções: horizontal, vertical e diagonal)
        # dx, dy representam a mudança nas coordenadas
        # custo representa o custo do movimento
        movimentos = [
            (0, 1, CUSTO_RETO),    # Direita
            (0, -1, CUSTO_RETO),   # Esquerda
            (1, 0, CUSTO_RETO),    # Baixo
            (-1, 0, CUSTO_RETO),   # Cima
            (1, 1, CUSTO_DIAGONAL),  # Diagonal inferior direita
            (1, -1, CUSTO_DIAGONAL), # Diagonal inferior esquerda
            (-1, 1, CUSTO_DIAGONAL), # Diagonal superior direita
            (-1, -1, CUSTO_DIAGONAL) # Diagonal superior esquerda
        ]

        for dx, dy, custo in movimentos: # calcula todas as posicoes dos vizinhos
            vizinho_x, vizinho_y = pos_atual[0] + dx, pos_atual[1] + dy
            pos_vizinho = (vizinho_x, vizinho_y)

            # Verifica se o vizinho está dentro dos limites da grade
            if not (0 <= vizinho_x < largura_grid and 0 <= vizinho_y < altura_grid):
                continue

            # Verifica se o vizinho é um obstáculo
            if pos_vizinho in obstaculos:
                continue

            # Calcula o g_score para o vizinho
            tentative_g_score = g_score + custo #custo real + custo do movimento

            # Se este é um caminho melhor para o vizinho, ou se o vizinho não foi visitado antes
            if tentative_g_score < g_score_map.get(pos_vizinho, float('inf')):
                g_score_map[pos_vizinho] = tentative_g_score #se tentative_g_score for melhor, registra ele no g_score
                h_vizinho = heuristica(pos_vizinho, pos_objetivo) # calcula a distancia ate o objetivo
                f_vizinho = tentative_g_score + h_vizinho #calcula o f_score total estimado
                
                novo_caminho = list(caminho_atual) + [pos_vizinho] # Cria uma copia do caminho ate pos_atual e depois adiciona o pos_vizinho a essa copia
                
                # Adiciona o vizinho ao open_set com as informacoes atualizadas(f_score, g_score,posicao e caminho que levou ate ele),
                # é candidato a ser o próximo nó a ser explorável
                heapq.heappush(open_set, (f_vizinho, tentative_g_score, pos_vizinho, novo_caminho))

    # Se o loop terminar e o objetivo não for alcançado, significa que não há caminho
    return []



