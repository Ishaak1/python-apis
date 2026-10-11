import sqlite3
from flask import Blueprint, jsonify
from utils import concat_genres_consoles, list_of_available_games

fetch_game_bp = Blueprint("get_game", __name__)

@fetch_game_bp.route("/game/<int:id>", methods=["GET"])
def get_game(id):

  db = sqlite3.connect("games.db")
  db.row_factory = sqlite3.Row
  cursor = db.cursor()

  wanted_game = []
  game_to_id, id_to_game = list_of_available_games()

  if id in game_to_id.values():

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
                        g.id = (?)""", [id])

    db.commit()
  
    wanted_game = [dict(game) for game in cursor.fetchall()]
    wanted_game = concat_genres_consoles(wanted_game)
  
    db.close()

    return jsonify(wanted_game[0]), 200
  
  else:

    db.close()

    return jsonify({"ERROR" : "Invalid game id"}), 404