import sqlite3
from flask import Blueprint, jsonify
from utils import list_of_available_own_statuses

delete_by_own_status_bp = Blueprint("delete_by_own_status", __name__)

@delete_by_own_status_bp.route("/games/ownership/<string:status>", methods=["DELETE"])
def delete_by_own_status(status):

  db = sqlite3.connect("games.db")
  db.row_factory = sqlite3.Row
  cursor = db.cursor()

  own_status_to_id, id_to_own_status = list_of_available_own_statuses()
  status = status.capitalize()

  if status in own_status_to_id.keys():

    id = own_status_to_id[status]

    cursor.execute("DELETE FROM games WHERE own_status_id = (?)", [id])

    db.commit()
    db.close()

  else:

    db.close()

    return jsonify({"ERROR": "Invalid ownsership status"}), 400

  return jsonify({"Removed" : True}), 200