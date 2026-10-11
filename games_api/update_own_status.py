import sqlite3
from flask import Blueprint, jsonify
from utils import list_of_available_own_statuses, list_of_available_games

update_own_status_bp = Blueprint("update_own_status", __name__)

@update_own_status_bp.route("/game/ownership/<int:id>/<string:status>", methods=["PATCH"])
def edit_game_own_status(id, status):

  db = sqlite3.connect("games.db")
  db.row_factory = sqlite3.Row
  cursor = db.cursor()

  status = status.capitalize()
  
  own_status_to_id, id_to_own_status = list_of_available_own_statuses()
  game_to_id, id_to_game = list_of_available_games()

  cursor.execute("SELECT own_status_id FROM games WHERE id = (?)", (id,))
  current_id = dict(cursor.fetchone())
  current_id = current_id["own_status_id"]
  current_own_status = id_to_own_status[current_id]

  if current_id in own_status_to_id.values():

    current_own_status = id_to_own_status[current_id]
  
  if id not in game_to_id.values():

    db.close()
    
    return jsonify({"ERROR": "Invalid id"}), 400

  if status in own_status_to_id.keys():

    own_status_id = own_status_to_id[status]

    cursor.execute("UPDATE games SET own_status_id = (?) WHERE id = (?)", [own_status_id, id])
    db.commit()
    db.close()

  else:

    db.close()

    return jsonify({"ERROR invalid own status": f"{id_to_own_status[1]}, {id_to_own_status[2]}, {id_to_own_status[3]}"})

  if current_own_status != status:
    
    return jsonify({"Success": f"Upated own status from {current_own_status} to {status}"})

  else: 

    return jsonify({"Warning": "Result remains unchanged"}), 200