import random
import time
import os
from pyamaze import maze, agent, textLabel, COLOR

# Função que diminui a velocidade q o texto é escrito no terminal
def diminui_velocidade_texto(texto, PouI, delay=0.001):
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

# Limpa terminal antes de rodar
os.system("clear")

# Contexto da história
diminui_velocidade_texto("Johan Towns (JT): Shells! Shells! Estão pedindo nossa ajuda em um caso...\nParece que na noite passada, uma obra de arte muito valiosa do museu Hermitage, aqui em São Petersburgo, foi roubada.\nE o culpado ainda não foi encontrado, porém com ajuda das autoridades locais, alguns suspeitos foram detidos.\nAgora querem nossa ajuda, o estimado Detetive Shells Shock, e seu fiel escudeiro Sr. Johan Towns!\nApenas nós conseguiríamos decifrar esse misté-\n\nShells Shock (SS): Está atrasado, caro Sr. Towns, já falei com as autoridades, e esse caso é mais simples do que parece,\njá tenho uma boa ideia de quem é o culpado, apenas com o que foi dito.", "P")

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
else:    
    diminui_velocidade_texto(f"\nSS: Caro Sr. Towns, o{comS} culpado{comS} {vl}: {', '.join(listaCulpados)}", "P")
    falaTelefone = "parece que os culpados, realmente quem você tinha dito ser, estão tentando fugir"
    
diminui_velocidade_texto(f"\nJT: Estou chocado com sua astúcia Detetive Shock, co-como chegou a esta conclu-\ntrrrim-trrrim-trrrim\nO telefone está tocando...", "P")
diminui_velocidade_texto(f"\nSS: Não irá atendê-lo Sr. Towns...?", "P")
diminui_velocidade_texto(f"\nJT: Ah, verdade, vou atender... Alô... uhum... entendi... estamos a caminho.\nShells, Shells, você não vai acreditar, eram as autoridades locais, {falaTelefone}, e pediram a nossa ajuda na captura. Vamos?", "P")
diminui_velocidade_texto(f"\nSS: Depois do senhor, Sr. Towns...", "P")
print("\033[3m(Ajude o Detevite Shocks e o Sr. Towns a capturar os culpados!)\033[0m")
    
# Criação do labirinto
labirinto = maze()
labirinto.CreateMaze(loopPercent=10, saveMaze=True)

# Lista com as posições ocupadas
posicoesOcupadas = set()

# Adicionando culpados no mapa, sempre em posições
for culpado in listaCulpados:
    while True:
        # Setando coordanadas aleatórias
        x = random.randint(1,10)
        y = random.randint(1,10)
        # Conferindo se a posição já está ocupada por outro suspeito
        if (x,y) not in posicoesOcupadas and (x,y) != (10,10):
            posicoesOcupadas.add((x,y))
            a = agent(labirinto,x,y,color=COLOR.red)
            break

# Criação do Jogador 
jogador = agent(labirinto, footprints=True)
labirinto.enableWASD(jogador)

# Função delay antes da próxima ação    
time.sleep(5)  # Pausa de 5 segundos

labirinto.run()
