import time
import os

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
        
# Função que limita valor de N
def pede_N():
    while True:
        try:
            # \033[3m e \033[0m deixa em itálico
            N = int(input("\033[3m(digite um valor entre 3 e 7):\033[0m "))
            if 3 <= N <= 7:
                return N
            else:
                print("\033[3m(número fora do intervalo, tente novamente)\033[0m")
        except ValueError:
            print("\033[3m(digite um número inteiro)\033[0m")

# Função que gera lista de supeitos
def gera_lista_suspeitos(N):
    lista = [chr(65 + i) for i in range(N)]
    return lista

# Limpa terminal antes de rodar
os.system("clear")

# Contexto da história
diminui_velocidade_texto("Johan Towns (JT): Shells! Shells! Estão pedindo nossa ajuda em um caso...\nParece que na noite passada, uma obra de arte muito valiosa do museu Hermitage, aqui em São Petersburgo, foi roubada.\nE o culpado ainda não foi encontrado, porém com ajuda das autoridades locais, alguns suspeitos foram detidos.\nAgora querem nossa ajuda, o estimado Detetive Shells Shock, e seu fiel escudeiro Sr. Johan Towns!\nApenas nós conseguiríamos decifrar esse misté-\n\nShells Shock (SS): Está atrasado, caro Sr. Towns, já falei com as autoridades, e esse caso é mais simples do que parece,\njá tenho um breve ideia de quem é o culpado, apenas com o que foi dito.", "P")

# N é o número de suspeitos, nossos vértices
diminui_velocidade_texto("\nJT: Estou chocado com sua astúcia Detetive Shock. Então, para começar, quantos suspeitos são exatamente?: ", "P")

N = pede_N()

diminui_velocidade_texto(f"SS: São exatamente {N} supeitos.", "P")

suspeitos = gera_lista_suspeitos(N)

diminui_velocidade_texto("\nJT: Então os suspeitos são:", "P")
diminui_velocidade_texto(', '.join(suspeitos), "P")
diminui_velocidade_texto("\nJT: Por gentileza Detetive, poderia me dizer o que cada suspeito está afirmando?", "P")

