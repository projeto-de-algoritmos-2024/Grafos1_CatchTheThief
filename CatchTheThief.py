import random
import time
import os
from pyamaze import maze, agent, textLabel, COLOR

# Função que diminui a velocidade q o texto é escrito no terminal
def diminui_velocidade_texto(texto, PouI, delay=0.05):
    for char in texto:
        print(char, end='', flush=True)
        time.sleep(delay)
    if PouI == "I":
        resposta = input()
        return resposta
    else:
        print()
        
# Função que limita valor de N (Número de suspeitos)
def pede_N():
    while True:
        try:
            # \033[3m e \033[0m deixa em itálico
            Numero = int(input(f"\033[3m(digite um valor entre 3 e 7):\033[0m "))
            if 3 <= Numero <= 7:
                return Numero
            else:
                print("\033[3m(número fora do intervalo, tente novamente)\033[0m")
        except ValueError:
            print("\033[3m(digite um número inteiro)\033[0m")

# Função que limita valor de M (Número de suspeitros dizendo a verdade)
def pede_M(N):
    while True:
        try:
            # \033[3m e \033[0m deixa em itálico
            Numero = int(input(f"\033[3m(digite um valor entre 1 e {N}):\033[0m "))
            if 1 <= Numero <= N:
                return Numero
            else:
                print("\033[3m(número fora do intervalo, tente novamente)\033[0m")
        except ValueError:
            print("\033[3m(digite um número inteiro)\033[0m")

# Função que gera dicionario de supeitos
def gera_dicionario_suspeitos(N):
    dicionario = {chr(65 + i): i for i in range(N)}
    return dicionario

# Função que gera a matriz zerada
def gera_matriz_zero(N):
    matriz = [[0 for i in range(N)] for i in range(N)]
    return matriz

# Função que determina quem acusa quem (1 = está sendo acusado / 0 = não está sendo acusado)
def quem_acusa_quem(matriz, quem_acusa, acusado, dicionario):
    linha = dicionario[quem_acusa]
    if acusado == "X":
        for coluna in range(len(matriz)):
            if coluna != linha:
                matriz[linha][coluna] = 1
    else:
        coluna = dicionario[acusado]
        matriz[linha][coluna] = 1

# Função que soma o total de cada coluna
def soma_coluna(matriz, coluna):
    soma = 0
    for linha in matriz:
        soma += linha[coluna]
    return soma

# Função que gera dicionário com a soma da coluna
def gera_dicionario_soma(N, matriz):
    dicionario = {chr(65 + i): soma_coluna(matriz, i) for i in range(N)}
    return dicionario

# Função que retorna os culpados
def gera_lista_culpados(M, dicionario):
    culpados = []
    for suspeito, soma in dicionario.items():
        if soma == M:
            culpados.append(suspeito)
    return culpados

# Função para calcular a célula vizinha
def pega_prox_celula(celula, direcao):
    x, y = celula
    if direcao == 'E':
        return (x, y + 1)
    elif direcao == 'W':
        return (x, y - 1)
    elif direcao == 'N':
        return (x - 1, y)
    elif direcao == 'S':
        return (x + 1, y)

# Função de busca e largura - BFS
# Retorna o menor caminho entre 2 pontos
def bfs_caminho(labirinto, comeco, fim):
    # Fila de vizinhos
    fila = [comeco]
    # Guarda de onde veio (pois será usado para fazer o caminho reverso) e já marca como visitado
    origem = {comeco: None}

    # Enquanto a fila tiver itens
    while fila:
        # Tirando o primeiro da fila
        atual = fila.pop(0)
        # Para quando chegar no destino
        if atual == fim:
            break
        # Para cada direção
        for direcao in 'ESNW':
            # Confere se o valor no dicionário é igual 1 (tem caminho livre)
            if labirinto.maze_map[atual][direcao] == 1:
                # Pega a próxima célula
                prox_celula = pega_prox_celula(atual, direcao)
                # Caso ainda não tenha sido visitado
                if prox_celula not in origem:
                    # Inserindo o vizinho na fila
                    fila.append(prox_celula)
                    # Marcando a origem da proxima célula com a atual
                    origem[prox_celula] = atual

    # Construindo caminho ao contrário
    caminho = []
    # Enquanto houver um destino
    while fim:
        # Insere o 'fim', que é o atual no caminho
        caminho.append(fim)
        # Pega a origem e transforma no novo fim
        fim = origem[fim]
        # Retorna o caminho reverso
    return caminho[::-1]

# Criando caminho completo
def caminho_completo(labirinto, lista):
    # Cirando lista vazia que vai guardar nosso caminho
    caminho_completo = []
    # Para cada item da lista
    for i in range(len(lista) - 1):
        # Atribuindo o caminho entre o primeiro e o segundo item da lista
        menor_caminho_entre_dois_pontos = bfs_caminho(labirinto, lista[i], lista[i + 1])
        # Adiciona esse pedaço do caminho no caminho completo, retirando o último elemento, pois ele já será o primeiro elemento na próxima iteração
        caminho_completo.extend(menor_caminho_entre_dois_pontos[:-1])
    # Adicionando último item da lista
    caminho_completo.append(lista[-1])
    return caminho_completo

# Limpa terminal antes de rodar
os.system("clear")

# Contexto da história
diminui_velocidade_texto("Johan Towns (JT): Shells! Shells! Estão pedindo nossa ajuda em um caso...\nParece que na noite passada, uma obra de arte muito valiosa do museu Hermitage, aqui em São Petersburgo, foi roubada.\nE o culpado ainda não foi encontrado, porém com ajuda das autoridades locais, alguns suspeitos foram detidos.\nAgora querem nossa ajuda, o estimado Detetive Shells Shock, e seu fiel escudeiro Sr. Johan Towns!\nApenas nós conseguiríamos decifrar esse misté-\n\nShells Shock (SS): Está atrasado, caro Sr. Towns, já falei com as autoridades, e esse caso é mais simples do que parece,\njá tenho uma boa ideia do que aconteceu, apenas com o que foi dito.", "P")

diminui_velocidade_texto("\nJT: Estou chocado com sua astúcia Detetive Shock. Então, para começar, quantos suspeitos são exatamente? ", "P")

# N é o número de suspeitos, nossos vértices
N = pede_N()

diminui_velocidade_texto(f"\nSS: São exatamente {N} supeitos.", "P")

# Gerando dicionário de suspeitos
suspeitos = gera_dicionario_suspeitos(N)

# Printando a lista de supeitos separados por vírgula
diminui_velocidade_texto("\nJT: Então os suspeitos são:", "P")
diminui_velocidade_texto(', '.join(suspeitos.keys()), "P")


diminui_velocidade_texto("\nJT: Por gentileza Detetive, poderia me dizer o que cada suspeito está afirmando?", "P")

# Gerando matriz que guardará quem acusou quem
matrizAcusacoes = gera_matriz_zero(N)

# Pedindo acusações para o usuário
for quem_acusa in suspeitos.keys():
    # Fazer até ser um suspeito válido
    while True: 
        # Pede para o usuário acusar, já vem em maiúsculo
        diminui_velocidade_texto(f"{quem_acusa} está acusando quem?", "P")
        acusado = input("\033[3m(digite a letra de quem está sendo acusado, ou digite X para acusar todos de uma vez) \033[0m").upper()
        # Se o acusado estiver na lista de suspeitos, ou a resposta seja X, chama a função que põe 1 na matriz 
        if (acusado in suspeitos and acusado != quem_acusa) or acusado == "X": 
            quem_acusa_quem(matrizAcusacoes, quem_acusa, acusado, suspeitos)
            break 
        else:
            # Se o acusado for um caracter inválido informa que não é um suspeito
            if acusado == quem_acusa:
                complemento = "não pode se auto acusar!!!"
            else:
                complemento = "não está na lista de suspeitos!!!"
            diminui_velocidade_texto(f"\033[3m('{acusado} {complemento}')\033[0m", "P") 

diminui_velocidade_texto("\nJT: Estou chocado com sua astúcia Detetive Shock, conseguiu lembrar exatamente o que foi dito por cada suspeito...\nE quantos estão dizendo a verdade?", "P")

diminui_velocidade_texto("\nSS: Não consigo afirmar com total certeza, porém creio que sejam...", "P")

# M é o número de suspeitos dizendo a verdade
M = pede_M(N)

# Gerando dicionário de somas
dicionarioSoma = gera_dicionario_soma(N, matrizAcusacoes)

# Gerando lista de culpados
listaCulpados = gera_lista_culpados(M, dicionarioSoma)

# Salvando o número de culpados
nCulpados = len(listaCulpados)

# If para trocar entre singular e plural dependendo do número de culpados
if nCulpados <= 1:
    vl = "é"
    comS = ""
else:
    vl = "são"
    comS = "s"

# Resto da história
diminui_velocidade_texto(f"\nJT: Porém é impossível descobrir quem {vl} o{comS} verdadeiro{comS} culpado{comS}, não é mesmo, Detetive, hahah-", "P")
diminui_velocidade_texto(f"\nSS: Aí que você se engana, Sr. Towns...\nJá sei exatamente o desfecho dessa história.", "P")
diminui_velocidade_texto(f"\nJT: Estou chocado com sua astúcia Detetive Shock, e qual seria?", "P")

if nCulpados == 0:
    diminui_velocidade_texto("\nSS: Nenhum dos suspeitos é o culpado.", "P")
    falaTelefone = "parece que o verdadeiro culpado está fugindo, de fato não era nenhum dos supeitos da nossa lista"
    seta = ""
else:    
    diminui_velocidade_texto(f"\nSS: Caro Sr. Towns, o{comS} culpado{comS} {vl}: {', '.join(listaCulpados)}", "P")
    falaTelefone = "parece que os culpados, realmente quem você tinha dito ser, estão tentando fugir"
    seta = " -> "
    
diminui_velocidade_texto(f"\nJT: Estou chocado com sua astúcia Detetive Shock, co-como chegou a esta conclu-\ntrrrim-trrrim-trrrim\nO telefone está tocando...", "P")
diminui_velocidade_texto(f"\nSS: Não irá atendê-lo Sr. Towns...?", "P")
diminui_velocidade_texto(f"\nJT: Ah, verdade, vou atender... Alô... uhum... entendi... estamos a caminho.\nShells, Shells, você não vai acreditar, eram as autoridades locais, {falaTelefone}, e pediram a nossa ajuda na captura. Vamos?", "P")
diminui_velocidade_texto(f"\nSS: Depois do senhor, Sr. Towns...", "P")
diminui_velocidade_texto(f"\nN: Após a ligação, o Detetive Shells Shock e seu fiel escudeiro Sr. Johan Towns, saem em busca do{comS} verdadeiro{comS} culpado{comS}.\nObviamente, com tamanha astúcia, o Detetive vai pelo melhor caminho... Já o atrapalhado Johan Towns...", "P")
print("\033[3m(Após ver o caminho do Detetive, ajude o pobre Sr. Towns a fazer o mesmo)\033[0m")
    
# Criação do labirinto
labirinto = maze(15, 15)
labirinto.CreateMaze(loopPercent=50)

# Lista com as posições ocupadas, já com a posição inicial
posicoesOcupadas = [(15, 15)]

# Quando não há culpados na lista, marca o verdeiro culpado no objetivo
if nCulpados == 0:
    z = agent(labirinto, 1, 1, color=COLOR.red)

# Adicionando culpados no mapa, sempre em posições
for culpado in listaCulpados:
    while True:
        # Setando coordanadas aleatórias
        x = random.randint(1,15)
        y = random.randint(1,15)
        # Conferindo se a posição já está ocupada por outro suspeito
        if (x,y) not in posicoesOcupadas:
            posicoesOcupadas.append((x,y))
            a = agent(labirinto,x,y,color=COLOR.red)
            break

# Adicionando posição final
posicoesOcupadas.append((1, 1))

# Criando melhor caminho
MelhorCaminho = caminho_completo(labirinto, posicoesOcupadas)

# Label com a quantidade de passos do melhor caminho
label = textLabel(labirinto,f"Quantidade de passos do melhor caminho, feito pelo Detetive nessa ordem: Começo -> {' -> '.join(listaCulpados)}{seta}Fim", len(MelhorCaminho) + 1)

# Mostrando melhor caminho
mostrandoMelhorCaminho = agent(labirinto, footprints=True, filled=True)
labirinto.tracePath({mostrandoMelhorCaminho: MelhorCaminho}, delay = 200, kill=True)

# Criando do Jogador 
jogador = agent(labirinto, footprints=True, color=COLOR.green)
labirinto.enableWASD(jogador)

# Função delay antes da próxima ação    
time.sleep(2)  # Pausa de 5 segundos

labirinto.run()