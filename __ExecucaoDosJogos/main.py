import sys
import os
from typing import List

# Adiciona o diretório 'DC-UFSCar-ES2-202401-Grupo3' ao PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import gamble.models as g


if __name__ == "__main__":
    while True:
        game_input = input("Selecione um jogo para jogar (BLACKJACK, BACARA): ")

        if game_input.upper() not in ["BLACKJACK", "BACARA"]:
            print("Selecione uma opção válida (BLACKJACK ou BACARA): ")
        else:
            break

    if game_input.upper() == "BLACKJACK":
        cards = g.BlackJackCard()
        players: List[g.BlackJackPlayer] = []

        qtd_players = int(input("Digite a quantidade de jogadores: "))

        for i in range(qtd_players):
            nome = input(f"Digite o nome do jogador {i + 1}: ")

            while True:
                try:
                    aposta = int(input(f"Digite a aposta do jogador {i}: "))
                    break
                except Exception:
                    print("Digite uma aposta válida")

            players.append(g.BlackJackPlayer(nome, aposta))

        game = g.BlackJackGame(players)
        game.start_game()

    elif game_input.upper() == "BACARA":
        player = g.BaccaratPlayer(balance=100)

        # Criando o jogo e passando o jogador
        game = g.BaccaratGame(player)

        # Loop principal do jogo
        while True:
            # Exibindo o saldo atual
            print(f"\nSaldo atual: {player.balance}")

            # Verificando se o jogador tem saldo suficiente
            if player.balance <= 0:
                print("Você ficou sem saldo. O jogo acabou.")
                break

            # Receber o valor da aposta
            try:
                bet_amount = float(input("Digite o valor da sua aposta: "))
                if bet_amount > player.balance:
                    print("Aposta maior que o saldo disponível. Tente novamente.")
                    continue
            except ValueError:
                print("Valor de aposta inválido. Tente novamente.")
                continue

            # Escolher em quem apostar (Player, Banker ou Tie)
            bet_on = input("Aposte em Player, Banker ou Tie: ").capitalize()

            # Verificando se a aposta é válida
            if bet_on not in ["Player", "Banker", "Tie"]:
                print("Escolha inválida. Tente novamente.")
                continue

            # Jogador faz a aposta
            try:
                player.place_bet(bet_amount, bet_on)
            except ValueError as e:
                print(e)
                continue

            # Jogando o jogo
            result = game.play_game()
            print(result)

            # Pergunta se o jogador deseja continuar
            keep_playing = input("Deseja jogar outra rodada? (s/n): ").lower()
            if keep_playing != 's':
                print("Obrigado por jogar!")
                break

            # Reiniciar o jogo
            game.reset_game()
