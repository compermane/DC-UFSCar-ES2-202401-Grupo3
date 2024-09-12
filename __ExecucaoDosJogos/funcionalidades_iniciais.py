import sys
import os
from typing import List

# Adiciona o diretório 'DC-UFSCar-ES2-202401-Grupo3' ao PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import gamble.models as g

def dados():
    dado = g.Dice()

    while True:
        action = input("Digite o que quer fazer com os dados (JOGAR (1), JOGAR VÁRIAS VEZES (2)): ")

        if action.upper() not in ["JOGAR", "JOGAR VÁRIAS VEZES", "1", "2"]:
            print("Digite uma ação válida")
            continue
        else:
            if action.upper() in ["JOGAR", "1"]:
                print(f"Resultado do lançamento de 2 dados de 6 faces: {dado.roll()}")
            else:
                while True:
                    try:
                        qtd = int(input("Digite a quantidade de vezes que se quer lançar o dado: "))
                        break
                    except:
                        print("Digite uma quantidade válida (inteiro)")
                print(f"Resultado de {qtd} lançamentos de 2 dados dados de 6 faces: {dado.roll_many(qtd)}")

        play_again = input("Deseja jogar novamente? (s/n): ")
        if play_again.upper() != "S":
            break

def poker():
    while True:
        deck = g.Deck(shuffle = True)
        hand = deck.draw_hand()

        print(f"A mão obtida foi {hand}. O seu rank é: {hand.rank.name} e tem o valor {hand.rank.value}")
        action = input("Deseja pegar outra mão? (s/n):")

        if action.upper() != "S":
            break

def golfe():
    YARDS = (332, 410, 357, 148, 431, 519, 338, 405, 283, 515, 348, 148, 446, 348, 380, 431, 217, 389)
    PAR = (4, 4, 4, 3, 4, 5, 4, 4, 4, 5, 4, 3, 4, 4, 4, 4, 3, 4)
    HANDICAP = (15, 3, 5, 17, 1, 9, 11, 7, 13, 6, 16, 18, 2, 14, 8, 4, 12, 10)
    HCC_DATA = zip(YARDS, PAR, HANDICAP, strict=True)

    while True:
        while True:
            try:
                qtd = int(input("Digite a quantidade de jogadores: "))
                break
            except:
                print("Digite um valor correto (inteiro)")

        players = []
        for i in range(qtd):
            nome = input(f"Digite o nome do jogador {i + 1}: ")
            handicap = input(f"Digite o handicap (nível de habiliadade) do jogador {i + 1}: ")
            players.append(g.Player(nome, handicap))

        course_name = input("Digite o nome do campo: ")
        holes = [g.Hole(index + 1, x[0], x[1], x[2]) for index, x in enumerate(HCC_DATA)]
        course = g.Course(course_name, holes)

        game = g.Group(course, players)
        print(f"O nome do campo é {game.course.name}, tem yards = {game.course.yards}, {len(game.course.holes)} holes e par = {game.course.par}")
        print("Os jogadores são:")
        for player in game.players:
            print(f"- {player.name}, handicap: {player.handicap}")

        action = input("Deseja iniciar outro jogo de golfe? (s/n): ")
        if action.upper() != "S":
            break

if __name__ == "__main__":
    while True:
        func = input("Digite a funcionalidade (DADOS, CARTAS, GOLFE): ")

        if func.upper() not in ["DADOS", "CARTAS", "GOLFE"]:
            print("Selecione uma opção válida (DADOS, CARTAS ou GOLFE)")
        else: 
            if func.upper() == "DADOS":
                dados()
            elif func.upper() == "CARTAS":
                poker()
            else:
                golfe()

        action = input("Gostaria de testar outra coisa? (s/n): ")
        if action.upper() != "S":
            break