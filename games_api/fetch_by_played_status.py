import sqlite3
from flask import Blueprint, jsonify
from utils import concat_genres_consoles, list_of_available_played_statuses

fetch_by_played_status_bp = Blueprint("fetch_by_played_status", __name__)

@fetch_by_played_status_bp.route("/games/played/<string:status>", methods=["GET"])
def fetch_by_played_status(status):

  db = sqlite3.connect("games.db")
  db.row_factory = sqlite3.Row
  cursor = db.cursor()

  status = status.capitalize()

  wanted_games = []
  played_status_to_id, id_to_played_status = list_of_available_played_statuses()

  if status in played_status_to_id.keys():

    id = played_status_to_id[status]

    cursor.execute("""SELECT
                        p.played_status,
                        g.id,
                        c.console,
                        o.own_status,
                        g.name,
                        ge.genre,
                        co.company
                      FROM
                        games g
                      JOIN
                        played_statuses p
                      ON
                        p.id = g.played_status_id
                      JOIN
                        own_statuses o
                      ON
                        o.id = g.own_status_id
                      JOIN
                        game_console gc
                      ON
                        g.id = gc.game_id
                      JOIN
                        consoles c
                      ON
                        c.id = gc.console_id
                      JOIN
                        game_genre gg
                      ON
                        gg.game_id = g.id
                      JOIN
                        genres ge
                      ON
                        ge.id = gg.genre_id
                      JOIN
                        companies co
                      ON
                        co.id = c.company_id
                      WHERE
                        p.id = (?)""", [id])

    db.commit()
  
    wanted_games = [dict(game) for game in cursor.fetchall()]
    wanted_games = concat_genres_consoles(wanted_games)
  
    db.close()

  else:
    
    db.close()

    return jsonify({"ERROR": "Invalid game id"}), 400

  return jsonify(wanted_games), 200