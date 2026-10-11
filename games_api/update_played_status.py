import sqlite3
from flask import Blueprint, jsonify, request
from utils import list_of_available_played_statuses, list_of_available_games

update_played_status_bp = Blueprint("update_played_status", __name__)

@update_played_status_bp.route("/game/played/<int:id>/<string:status>", methods=["PATCH"])
def update_played_status(id, status):

  db = sqlite3.connect("games.db")
  db.row_factory = sqlite3.Row
  cursor = db.cursor()

  status = status.capitalize()
  
  played_status_to_id, id_to_played_status = list_of_available_played_statuses()
  game_to_id, id_to_game = list_of_available_games()

  cursor.execute("SELECT played_status_id FROM games WHERE id = (?)", (id,))
  current_id = dict(cursor.fetchone())
  current_id = current_id["played_status_id"]
  current_played_status = id_to_played_status[current_id]

  if current_id in played_status_to_id.values():

    current_played_status = id_to_played_status[current_id]
  
  if id not in game_to_id.values():

    db.close()
    
    return jsonify({"ERROR": "Invalid id"}), 400

  if status in played_status_to_id.keys():

    played_status_id = played_status_to_id[status]

    cursor.execute("UPDATE games SET played_status_id = (?) WHERE id = (?)", [played_status_id, id])
    db.commit()
    db.close()

  else:

    db.close()

    return jsonify({"ERROR invalid own status": f"{id_to_played_status[1]}, {id_to_played_status[2]}, {id_to_played_status[3]}"})

  if current_played_status != status:
    
    return jsonify({"Success": f"Upated own status from {current_played_status} to {status}"}), 200

  else: 

    return jsonify({"Warning": "Result remains unchanged"}), 200