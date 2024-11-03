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

# Limpa terminal antes de rodar
os.system("clear")

diminui_velocidade_texto("Johan Towns (JT): Shells! Shells! Estão pedindo nossa ajuda em um caso...\nParece que na noite passada, uma obra de arte muito valiosa do museu Hermitage, aqui em São Petersburgo, foi roubada.\nE o culpado ainda não foi encontrado, porém com ajuda das autoridades locais, alguns suspeitos foram detidos.\nAgora querem nossa ajuda, o infame Detetive Shells Shock, e seu fiel escudeiro Sr. Johan Towns!\nApenas nós conseguiríamos decifrar esse misté-\n\nShells Shock (SS): Está atrasado, caro Sr. Towns, já falei com as autoridades, e esse caso é mais simples do que parece, já tenho um breve ideia do quem é o culpado, apenas com o que foi falado.", "P")

# N é o número de suspeitos, nossos vértices
N = diminui_velocidade_texto("\nJT: Estou chocado com sua astúcia Detetive Shock. Então, para começar, quantos suspeitos são exatamente? ", "I")
diminui_velocidade_texto(f"SS: São exatamente {N} supeitos.", "P")



diminui_velocidade_texto(f"\nN: Então os suspeitos são: Por gentileza Detetive, poderia nos dizer o que cada suspeito está afirmando?", "P")

