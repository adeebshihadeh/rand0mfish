import json
from bot import Bot
from lichess import Lichess

token = open("token").read()

bot = Bot()
l = Lichess(token)


while True:
  print "streaming events..."

  for ev in l.stream_events().iter_lines():

    if ev == '': continue

    ev = json.loads(ev)

    if ev["type"] == "challenge":
      if bot.acceptable_challenge(ev["challenge"]):
        print "accepting challenge from", ev["challenge"]["challenger"]["id"]
        l.accept_challenge(ev["challenge"]["id"])
      else:
        print "rejecting challenge from", ev["challenge"]["challenger"]["id"]
        print "\t", ev["challenge"]["variant"]["name"], ev["challenge"]["timeControl"]
        l.decline_challenge(ev["challenge"]["id"])
    elif ev["type"] == "gameStart":
      print "game start"

      last_move = "last move"

      for e in l.stream_game_state(ev["game"]["id"]).iter_lines():
        if e == '': continue

        e = json.loads(e)

        # ignore chat
        if e["type"] == "chatLine": continue

        if e["type"] == "gameFull":
          moves = e["state"]["moves"]
        else:
          moves = e["moves"]
        moves = moves.encode("ascii", "ignore").split(" ")

        if last_move == moves[-1]: continue

        move = bot.get_move(moves)

        # game over
        if move is None: break

        if l.make_move(ev["game"]["id"], move).status_code == 200: last_move = str(move)

      print "game over"

