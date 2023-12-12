from SiiliCamController import SiiliCameraController
from pprint import pprint, pformat
from flask import Flask, request, jsonify

app = Flask(__name__)
siilicamController = SiiliCameraController()
steamIdToPc = dict()

stateData = dict()
stateData["steamId"] = 0
stateData["pcId"] = -1
stateData["isHidden"] = -1

siiliCamToControl = "tournament siili"

def get_selected_player(players):
    for player_id, playerdata in players.items():
            if playerdata["selected_unit"]:
                return player_id
    return None


@app.route('/spectator', methods=['POST'])
def spectator_endpoint():
    data = request.json
    if not ("hero" in data.keys() and "player" in data.keys()):
        return jsonify({"message": "bad!"}), 400
    playerdata = data["player"]
    #pprint(playerdata)
    steamids = []
    for team,  players in playerdata.items():
        for playerid, player in players.items():
            #print(player)
            steamids.append(player["steamid"])
    print(steamids)
    return {"message": "good"}, 400

  
if __name__ == '__main__':
    app.run(port=6043)