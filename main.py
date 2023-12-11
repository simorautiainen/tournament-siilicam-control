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
    herodata = data["hero"]
    playerdata = data["player"]
    #pprint(pformat(data))
    steamid = ""
    for team_name, players in herodata.items():
        selected_player = get_selected_player(players)
        if selected_player != None:
            playerinfo = playerdata[team_name][selected_player]
            name = playerinfo["name"]
            steamid = playerinfo["steamid"]
            heroname = herodata[team_name][selected_player]['name']
            print(f"Spectating {name}, {steamid}, {heroname }")
            break
    if len(steamid) > 0:
        if steamid in steamIdToPc.keys():
            try:
                pcId = steamIdToPc[steamid]
                if pcId != stateData["pcId"]:
                    result = siilicamController.set_camera_source_substring(siiliCamToControl, f"pc{steamIdToPc[steamid]}")
                    
                    if result != None:
                        siilicamController.set_camera_visibility(siiliCamToControl, True)
                        stateData["isHidden"] = False
                        stateData["pcId"] = pcId
                elif stateData["isHidden"] == True:
                    siilicamController.set_camera_visibility(siiliCamToControl, True)
                    stateData["isHidden"] = False
                    
            except Exception as e:
                print(f"could not set camera {e}")
        else:
            if stateData["isHidden"] != True:
                stateData["isHidden"] = True
                siilicamController.set_camera_visibility(siiliCamToControl, False)
            print(f"player gsi not setupped properly with steamid {steamid}")
    else:
        if stateData["isHidden"] != True:
            print("sending hidden")
            stateData["isHidden"] = True
            siilicamController.set_camera_visibility(siiliCamToControl, False)

    return {"message": "good"}, 400

@app.route('/pc', methods=['POST'])
def pc_endpoint():
    try:
        pc_id = request.args.get('pcId', default=-1, type=int)
        print("pcid:", pc_id)
        if pc_id < 0 or pc_id > 9:
            return jsonify({"message": "Invalid pcId. Must be between 0 and 9."}), 400
    except:
        print("could not parse pcid")
        return jsonify({"message": "Invalid pcId. Must be between 0 and 9."}), 400
    
    data = request.json
    print(data)
    try:
        steamId = data["player"]["steamid"]
        steamIdToPc[steamId] = pc_id
        print(steamIdToPc)
    except:
        print("could not parse steam id")
        return jsonify({"message": "could not parse steam id"}), 400
    # Perform actions based on the pcId
    # For example, just returning the pcId for now
    return jsonify({"message": f"Received pcId: {pc_id}"}), 200
  
if __name__ == '__main__':
    app.run(port=6043)