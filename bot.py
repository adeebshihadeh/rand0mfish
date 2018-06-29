import chess
from random import choice, getrandbits
from stockfish import Stockfish

stockfish = Stockfish()

def get_move(moves):
  b = chess.Board()

  if moves[0] == '': moves = [] 
  for m in moves:
    b.push(chess.Move.from_uci(m))

  if len(list(b.legal_moves)) < 1: return None


  # random move
  if bool(getrandbits(1)): return choice(list(b.legal_moves))

  # stockfish move
  stockfish.set_position(moves)

  return stockfish.get_best_move()
