import sqlite3
from flask import Blueprint, jsonify, request
from utils import validation_for_adding_game, create_console_genre_statement, create_game_statement

add_game_bp = Blueprint("add_game", __name__)

@add_game_bp.route("/game", methods=["POST"])
def add_game():

  db = sqlite3.connect("games.db")
  db.row_factory = sqlite3.Row
  cursor = db.cursor()

  body = request.json
  is_dict = isinstance(body, dict)

  if is_dict:

    information = validation_for_adding_game(body)

    if len(information) > 0:

      keys, update = create_game_statement(information)
      games_execution = ", ".join(keys)

      cursor.execute(f"INSERT INTO games (name, played_status_id, own_status_id) VALUES {games_execution}", update)
      db.commit()

      cursor.execute(f"SELECT id, name FROM games WHERE name = (?)", [information["name"]])
      games = [dict(info) for info in cursor.fetchall()]
      db.commit()

      name_to_id = {game["name"] : game["id"] for game in games}

      consoles_statement, genres_statement, consoles_list, genres_list = create_console_genre_statement(information, name_to_id)

      genres_placeholder = ", ".join(genres_statement)
      consoles_placeholder = ", ".join(consoles_statement)

      cursor.execute(f"INSERT INTO game_genre (game_id, genre_id) VALUES {genres_placeholder}", genres_list)
      db.commit()

      cursor.execute(f"INSERT INTO game_console (game_id, console_id) VALUES {consoles_placeholder}", consoles_list)
      db.commit()

    else:

      return jsonify({"ERROR": "Tried to add something invalid"}), 400

  else:

    return jsonify({"ERROR": "Invalid format returned from body"}), 400

  db.close()

  return jsonify({"status": "added games"}), 201