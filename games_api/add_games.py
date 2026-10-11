import sqlite3
from flask import Blueprint, jsonify, request
from utils import validation_for_adding_game, create_console_genre_statement, create_game_statement

add_games_bp = Blueprint("add_games", __name__)

@add_games_bp.route("/games", methods=["POST"])
def add_games():

  db = sqlite3.connect("games.db")
  db.row_factory = sqlite3.Row
  cursor = db.cursor()

  body = request.json
  is_list = isinstance(body, list)

  if is_list:

    list_of_information = []
    games_update = []
    games_insert = []
  
    for game in body:

      information = validation_for_adding_game(game)
      list_of_information.append(information)
      keys, update = create_game_statement(information)
      games_insert.extend(keys)
      games_update.extend(update)

    if len(list_of_information) > 0:

      games_execution = ", ".join(games_insert)
      cursor.execute(f"INSERT INTO games (name, played_status_id, own_status_id) VALUES {games_execution}", games_update)
      db.commit()

      names = []
      placeholders_list = []

      for info in list_of_information:
        
        names.append(info["name"])
        placeholders_list.append("?")

      placeholders_join = ", ".join(placeholders_list)
      placeholders = f"({placeholders_join})"

      cursor.execute(f"SELECT id, name FROM games WHERE name IN {placeholders}", names)
      db.commit()

      games_ids = [dict(info) for info in cursor.fetchall()]
      name_to_id = {game["name"] : game["id"] for game in games_ids}

      consoles_insert = []
      consoles_update = []
      genres_insert = []
      genres_update = []

      for info in list_of_information:

        consoles_statement, genres_statement, consoles_list, genres_list = create_console_genre_statement(info, name_to_id)

        consoles_insert.extend(consoles_statement)
        consoles_update.extend(consoles_list)
        genres_insert.extend(genres_statement)
        genres_update.extend(genres_list)

      genres_placeholder = ", ".join(genres_insert)
      consoles_placeholder = ", ".join(consoles_insert)

      cursor.execute(f"INSERT INTO game_genre (game_id, genre_id) VALUES {genres_placeholder}", genres_update)
      db.commit()

      cursor.execute(f"INSERT INTO game_console (game_id, console_id) VALUES {consoles_placeholder}", consoles_update)
      db.commit()

    else:

      return jsonify({"ERROR": "Tried to add something invalid"}), 400

  else:

    return jsonify({"ERROR": "Invalid format returned from body"}), 400

  db.close()

  return jsonify({"status": "added games"}), 201