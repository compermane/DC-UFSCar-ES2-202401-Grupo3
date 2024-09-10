"""
golf related games
"""

YARDS = (
    332,
    410,
    357,
    148,
    431,
    519,
    338,
    405,
    283,
    515,
    348,
    148,
    446,
    348,
    380,
    431,
    217,
    389,
)
PAR = (4, 4, 4, 3, 4, 5, 4, 4, 4, 5, 4, 3, 4, 4, 4, 4, 3, 4)
HANDICAP = (15, 3, 5, 17, 1, 9, 11, 7, 13, 6, 16, 18, 2, 14, 8, 4, 12, 10)
HCC_DATA = zip(YARDS, PAR, HANDICAP, strict=True)


class Hole:
    """
    a golf hole object
    """

    def __init__(self, tee: int, yards: int, par: int, handicap: int) -> None:
        """
        hole constructor

        Args:
            tee: the tee number for this hole
            yards: the number of yards from tee to hole
            par: the par for this hole
            handicap: the handicap value for this hole
        """
        self.tee = tee
        self.yards = yards
        self.par = par
        self.handicap = handicap


class Course:
    """
    a golf course object

    Args:
        name: the name of this golf course
        holes: a list of holes in this golf course
    """

    def __init__(self, name: str, holes: list[Hole]) -> None:
        self.name = name
        self.holes = sorted(holes, key=lambda hole: hole.tee)
        self.yards = sum(x.yards for x in self.holes)
        self.par = sum(x.par for x in self.holes)
        self.front = self.holes[:9]
        self.back = self.holes[9:]


class Player:
    """
    a golf player object

    Args:
        name: the name of the player
        handicap: the handicap of the player
    """

    def __init__(self, name: str, handicap: int) -> None:
        self.name = name
        self.handicap = handicap


class Group:
    """
    a golf group object

    Args:
        course: the course that this group is playing
        players: the list of players in this group
    """

    def __init__(self, course: Course, players: list[Player]) -> None:
        self.course = course
        self.players = players
        self.scores = {player.name: [None] * len(course.holes) for player in players}  # Inicia scores com None

    def add_score(self, player_name: str, hole_number: int, score: int):
        if player_name in self.scores and 1 <= hole_number <= len(self.scores[player_name]):
            self.scores[player_name][hole_number - 1] = score

    def get_total_score(self, player_name: str) -> int:
        scores = self.scores.get(player_name, [])
        return sum(score for score in scores if score is not None)

    def display_scores(self):
        for player_name, scores in self.scores.items():
            print(f"Scores for {player_name}:")
            for i, score in enumerate(scores):
                if score is not None:
                    print(f"  Hole {i + 1}: {score}")
                else:
                    print(f"  Hole {i + 1}: No score")
            print(f"  Total Score: {self.get_total_score(player_name)}")

    def declare_winner(self):
        if not self.players:
            print("No players in the group.")
            return

        # Determina a menor pontuação
        sorted_players = sorted(self.players, key=lambda p: self.get_total_score(p.name))
        min_score = self.get_total_score(sorted_players[0].name)
        
        # Verifica se há um empate
        winners = [player.name for player in sorted_players if self.get_total_score(player.name) == min_score]
        
        if len(winners) == 1:
            print(f"The winner is {winners[0]} with a score of {min_score}!")
        else:
            print(f"It's a tie between {' and '.join(winners)} with a score of {min_score}!")




HOLES = [Hole(index + 1, x[0], x[1], x[2]) for index, x in enumerate(HCC_DATA)]
HCC = Course("Hillcrest", HOLES)

import unittest

class TestGolfGame(unittest.TestCase):
    
    def test_course_setup(self):
        course = HCC
        self.assertEqual(course.yards, 6445)
        self.assertEqual(course.par, 71)

    def test_add_and_display_scores(self):
        # Setup
        player1 = Player("John", 10)
        player2 = Player("Alice", 15)
        group = Group(HCC, [player1, player2])

        # Adiciona scores para múltiplos buracos
        group.add_score("John", 1, 4)
        group.add_score("John", 2, 5)
        group.add_score("John", 3, 4)
        group.add_score("John", 4, 3)
        group.add_score("Alice", 1, 3)
        group.add_score("Alice", 2, 8)
        group.add_score("Alice", 3, 4)
        group.add_score("Alice", 4, 3)

        # Verifica se os scores foram adicionados corretamente
        self.assertEqual(group.scores["John"][0], 4)
        self.assertEqual(group.scores["John"][1], 5)
        self.assertEqual(group.scores["John"][2], 4)
        self.assertEqual(group.scores["John"][3], 3)
        self.assertEqual(group.scores["Alice"][0], 3)
        self.assertEqual(group.scores["Alice"][1], 8)
        self.assertEqual(group.scores["Alice"][2], 4)
        self.assertEqual(group.scores["Alice"][3], 3)

        # Verifica a pontuação total
        self.assertEqual(group.get_total_score("John"), 16)
        self.assertEqual(group.get_total_score("Alice"), 18)

        # Exibe os scores
        group.display_scores()

        # Declara o vencedor
        group.declare_winner()

    def test_incomplete_scores(self):
        player1 = Player("Bob", 12)
        player2 = Player("Sue", 14)
        group = Group(HCC, [player1, player2])

        # Adiciona scores para alguns buracos apenas
        group.add_score("Bob", 1, 5)
        group.add_score("Bob", 2, 4)
        group.add_score("Sue", 1, 4)
        group.add_score("Sue", 2, 5)

        # Espera-se que os jogadores não tenham scores para todos os buracos
        self.assertIsNone(group.scores["Bob"][2])
        self.assertIsNone(group.scores["Sue"][2])

        # Verifica a pontuação total
        self.assertEqual(group.get_total_score("Bob"), 9)
        self.assertEqual(group.get_total_score("Sue"), 9)

        # Exibe os scores
        group.display_scores()

        # Declara o vencedor
        group.declare_winner()

    def test_tie_score(self):
        player1 = Player("Tom", 8)
        player2 = Player("Jerry", 9)
        group = Group(HCC, [player1, player2])

        # Adiciona scores para múltiplos buracos com resultado empatado
        group.add_score("Tom", 1, 4)
        group.add_score("Tom", 2, 4)
        group.add_score("Tom", 3, 4)
        group.add_score("Tom", 4, 4)
        group.add_score("Jerry", 1, 4)
        group.add_score("Jerry", 2, 4)
        group.add_score("Jerry", 3, 4)
        group.add_score("Jerry", 4, 4)

        # Verifica a pontuação total
        self.assertEqual(group.get_total_score("Tom"), 16)
        self.assertEqual(group.get_total_score("Jerry"), 16)

        # Exibe os scores
        group.display_scores()

        # Declara o vencedor
        group.declare_winner()

    def test_extreme_scores(self):
        player1 = Player("Max", 5)
        player2 = Player("Emma", 6)
        group = Group(HCC, [player1, player2])

        # Adiciona scores extremos
        group.add_score("Max", 1, 1)
        group.add_score("Max", 2, 1)
        group.add_score("Max", 3, 1)
        group.add_score("Max", 4, 1)
        group.add_score("Emma", 1, 10)
        group.add_score("Emma", 2, 10)
        group.add_score("Emma", 3, 10)
        group.add_score("Emma", 4, 10)

        # Verifica a pontuação total
        self.assertEqual(group.get_total_score("Max"), 4)
        self.assertEqual(group.get_total_score("Emma"), 40)

        # Exibe os scores
        group.display_scores()

        # Declara o vencedor
        group.declare_winner()

    def test_multiple_rounds(self):
        player1 = Player("John", 10)
        player2 = Player("Alice", 15)
        group1 = Group(HCC, [player1, player2])
        group2 = Group(HCC, [player1, player2])

        # Adiciona scores para múltiplas rodadas
        group1.add_score("John", 1, 4)
        group1.add_score("John", 2, 5)
        group1.add_score("John", 3, 4)
        group1.add_score("Alice", 1, 3)
        group1.add_score("Alice", 2, 6)
        group1.add_score("Alice", 3, 4)

        group2.add_score("John", 1, 3)
        group2.add_score("John", 2, 4)
        group2.add_score("John", 3, 5)
        group2.add_score("Alice", 1, 4)
        group2.add_score("Alice", 2, 5)
        group2.add_score("Alice", 3, 6)

        # Verifica as pontuações totais para as duas rodadas
        self.assertEqual(group1.get_total_score("John"), 13)
        self.assertEqual(group1.get_total_score("Alice"), 13)
        self.assertEqual(group2.get_total_score("John"), 12)
        self.assertEqual(group2.get_total_score("Alice"), 15)

        # Exibe os scores e declara vencedores
        print("Group 1 Results:")
        group1.display_scores()
        group1.declare_winner()

        print("Group 2 Results:")
        group2.display_scores()
        group2.declare_winner()

if __name__ == "__main__":
    unittest.main()
