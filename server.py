import requests
import json

from bot import Bot

bot = Bot()

token = open("token").read()

header = {
  "Authorization": "Bearer {}".format(token)
}


url = "https://lichess.org/"
endpoints = {
  "events": "/api/stream/event",
  "game_state": "/api/bot/game/stream/{}",
  "accept_challenge": "/api/challenge/{}/accept",
  "decline_challenge": "/api/challenge/{}/decline",
  "make_move": "/api/bot/game/{}/move/{}"
}


def get(endpoint):
  return requests.get(url + endpoint, headers=header, stream=True)

def post(endpoint):
  return requests.post(url + endpoint, headers=header)

def stream_events():
  return get(endpoints["events"])

def stream_game_state(id):
  return get(endpoints["game_state"].format(id))

def accept_challenge(id):
  return post(endpoints["accept_challenge"].format(id))

def decline_challenge(id):
  return post(endpoints["decline_challenge"].format(id))

def make_move(id, move):
  return post(endpoints["make_move"].format(id, move))



while True:
  print "streaming events..."

  for ev in stream_events().iter_lines():
    try:
      ev = json.loads(ev)
    except:
      continue

    if ev["type"] == "challenge":
      if bot.acceptable_challenge(ev["challenge"]):
        print "accepting challenge from", ev["challenge"]["challenger"]["id"]
        accept_challenge(ev["challenge"]["id"])
      else:
        print "rejecting challenge from", ev["challenge"]["challenger"]["id"]
        decline_challenge(ev["challenge"]["id"])
    elif ev["type"] == "gameStart":
      print "game start"

      last_move = "last move"

      for e in stream_game_state(ev["game"]["id"]).iter_lines():
        try:
          e = json.loads(e)
        except:
          continue

        if e["type"] == "chatLine": continue

        if e["type"] == "gameFull":
          moves = e["state"]["moves"]
        else:
          moves = e["moves"]
        moves = moves.encode("ascii", "ignore").split(" ")

        if last_move == moves[-1]: continue

        move = bot.get_move(moves)

        if move is None:
          print "game overaaaa"
          break # game over
        else:
          last_move = str(move)
          make_move(ev["game"]["id"], move)

      print "finished game"
    else:
      print ev["type"]
