import sqlite3
from flask import Blueprint, jsonify, request
from utils import list_of_available_games

update_name_bp = Blueprint("update_name", __name__)

@update_name_bp.route("/game/name/<int:id>", methods=["PATCH"])
def update_name(id):

  db = sqlite3.connect("games.db")
  db.row_factory = sqlite3.Row
  cursor = db.cursor()

  body = request.json

  game_to_id, id_to_game = list_of_available_games()
  cursor.execute("SELECT * FROM games WHERE id = (?)", (id,))
  game = dict(cursor.fetchone())
  current_game = game["name"]

  if id not in game_to_id.values():

    db.close()
     
    return jsonify({"ERROR": "Invalid id"}), 400

  if "name" in body.keys():
    
    cursor.execute("UPDATE games SET name = (?) WHERE id = (?)", [body["name"], id])
    db.commit()
    db.close()

  else:
    
    db.close()
  
    return jsonify({"ERROR": "Key doesn't exist"}), 400

  return jsonify({"Success": f"Name was updated from {current_game} to {body['name']}"}), 200 
