import requests


url = "https://lichess.org/"
endpoints = {
  "events": "/api/stream/event",
  "game_state": "/api/bot/game/stream/{}",
  "accept_challenge": "/api/challenge/{}/accept",
  "decline_challenge": "/api/challenge/{}/decline",
  "make_move": "/api/bot/game/{}/move/{}"
}

class Lichess:
  def __init__(self, token):
    self.token = token
    self.header = {
      "Authorization": "Bearer {}".format(self.token)
    }

  def get(self, endpoint):
    return requests.get(url + endpoint, headers=self.header, stream=True)

  def post(self, endpoint):
    return requests.post(url + endpoint, headers=self.header)

  def stream_events(self):
    return self.get(endpoints["events"])

  def stream_game_state(self, id):
    return self.get(endpoints["game_state"].format(id))

  def accept_challenge(self, id):
    return self.post(endpoints["accept_challenge"].format(id))

  def decline_challenge(self, id):
    return self.post(endpoints["decline_challenge"].format(id))

  def make_move(self, id, move):
    return self.post(endpoints["make_move"].format(id, move))
