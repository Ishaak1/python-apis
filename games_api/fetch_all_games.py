import sqlite3
from flask import Blueprint, jsonify
from utils import concat_genres_consoles

fetch_games_bp = Blueprint("get_all_games", __name__)

@fetch_games_bp.route("/games", methods=["GET"])
def get_all_games():

  db = sqlite3.connect("games.db")
  db.row_factory = sqlite3.Row
  cursor = db.cursor()

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
                      co.id = c.company_id""")
  
  db.commit()

  games = [dict(game) for game in cursor.fetchall()]
  games = concat_genres_consoles(games)
  
  db.close()

  return jsonify(games), 200