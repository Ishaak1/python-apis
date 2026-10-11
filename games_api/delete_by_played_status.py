import sqlite3
from flask import Blueprint, jsonify
from utils import list_of_available_played_statuses

delete_by_played_status_bp = Blueprint("delete_by_played_status", __name__)

@delete_by_played_status_bp.route("/games/played/<string:status>", methods=["DELETE"])
def delete_by_played_status(status):

  db = sqlite3.connect("games.db")
  db.row_factory = sqlite3.Row
  cursor = db.cursor()

  played_status_to_id, id_to_played_status = list_of_available_played_statuses()
  status = status.capitalize()

  if status in played_status_to_id.keys():

    id = played_status_to_id[status]

    cursor.execute("DELETE FROM games WHERE played_status_id = (?)", [id])
    
    db.commit()
    db.close()

  else:

    db.close()

    return jsonify({"ERROR": "Invalid played status id"}), 400

  return jsonify({"Removed" : True}), 200