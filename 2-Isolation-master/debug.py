from isolation import Board
from sample_players import GreedyPlayer
from sample_players import RandomPlayer
from game_agent import CustomPlayer
from sample_players import null_score

player1 = CustomPlayer(3, null_score, True, 'minimax')
player2 = GreedyPlayer()
game = Board(player1, player2)

 
game.apply_move((2, 3))
game.apply_move((0, 5))



winner, history, outcome = game.play()   

print('student agent with 3 depths, null_score, iterative and minimax VS GreedyPlayer')
print("\nWinner: {}\nOutcome: {}".format(winner, outcome))
print(game.to_string())
print("Move history:\n{!s}".format(history))