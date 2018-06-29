import chess
from random import choice, getrandbits
from stockfish import Stockfish


class Bot():
  def __init__(self):
    self.stockfish = Stockfish()

  def acceptable_challenge(self, chall):
    if chall["variant"]["key"] != "standard":
      return False

    if chall["timeControl"]["limit"] >= 60:
      return False

    if chall["timeControl"]["increment"] > 0:
      return False

    return True

  def get_move(self, moves):
    b = chess.Board()

    if moves[0] == '': moves = [] 
    for m in moves:
      b.push(chess.Move.from_uci(m))

    if len(list(b.legal_moves)) < 1: return None

    # random move
    if bool(getrandbits(1)): return choice(list(b.legal_moves))

    # stockfish move
    self.stockfish.set_position(moves)

    return self.stockfish.get_best_move()
