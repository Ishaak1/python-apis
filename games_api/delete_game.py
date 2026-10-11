import sqlite3
from flask import Blueprint, jsonify
from utils import list_of_available_games

delete_game_bp = Blueprint("delete_game", __name__)

@delete_game_bp.route("/game/<int:remove>", methods=["DELETE"])
def delete_game(remove):

  db = sqlite3.connect("games.db")
  db.row_factory = sqlite3.Row
  cursor = db.cursor()
  
  game_to_id, id_to_game = list_of_available_games()
  
  if remove in game_to_id.values():

    cursor.execute("DELETE FROM games WHERE id = (?)", [remove])
    
    db.commit()
    db.close()

  else:
  
    db.close()

    return jsonify({"ERROR": "Invalid game id"}), 400

  db.close()

  return jsonify({"Removed" : True}), 200