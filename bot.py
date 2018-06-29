import chess
from random import choice
from stockfish import Stockfish


def get_move(moves):
  b = chess.Board()

  if moves[0] == '': moves = [] 
  for m in moves:
    b.push(chess.Move.from_uci(m))

  if len(list(b.legal_moves)) < 1: return None

  return choice(list(b.legal_moves))
