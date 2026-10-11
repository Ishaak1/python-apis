import sqlite3
from flask import Blueprint, jsonify, request
from utils import list_of_available_games, list_of_available_own_statuses, list_of_available_played_statuses, list_of_available_genres, list_of_available_consoles

update_game_bp = Blueprint("update_game", __name__)

@update_game_bp.route("/game/<int:game_id>", methods=["PATCH"])
def update_game(game_id):

  db = sqlite3.connect("games.db")
  db.row_factory = sqlite3.Row
  cursor = db.cursor()

  game_to_id, id_to_game = list_of_available_games()

  if game_id not in game_to_id.values():

    return jsonify({"ERROR": "Game doesn't exist"}), 404
  
  body = request.json
  information = validation(body)

  if len(information) > 0:

    execution, update, consoles_statement, genres_statement, consoles_update, genres_update = create_statement(information, game_id)
    
    if "name" in information.keys() or "played_status" in information.keys() or "own_status" in information.keys():
      
      update.append(game_id)
      cursor.execute(f"UPDATE games SET {execution} WHERE id = (?)", update)
      db.commit()
    
    if "genres" in information.keys():

      cursor.execute("DELETE FROM game_genre WHERE game_id = (?)", [game_id])
      db.commit()

      cursor.execute(f"INSERT INTO game_genre (game_id, genre_id) VALUES {genres_statement} ", genres_update)
      db.commit()
    
    if "consoles" in information.keys():
      
      cursor.execute("DELETE FROM game_console WHERE game_id = (?)", [game_id])
      db.commit()

      cursor.execute(f"INSERT INTO game_console (game_id, console_id) VALUES {consoles_statement}", consoles_update)
      db.commit()

  db.close()
  return jsonify({"Updated": True}), 200

def create_statement(information, game_id):

  keys = []
  update = []
  consoles_statement = []
  genres_statement = []
  consoles_update = []
  genres_update = []
  
  for key, value in information.items():
    
    if key == "name":

      keys.append("name = (?)")
      update.append(value)

    elif key == "played_status":

      keys.append("played_status_id = (?)")
      update.append(value)

    elif key == "own_status":

      keys.append("own_status_id = (?)")
      update.append(value)

    elif key == "consoles":

      for item in value:

        consoles_statement.append("(?, ?)")
        consoles_update.append(game_id)
        consoles_update.append(item)

    elif key == "genres":

      for item in value:
        
        genres_statement.append("(?, ?)")
        genres_update.append(game_id)
        genres_update.append(item)

  execution = ", ".join(keys)
  consoles_statement_string = ", ".join(consoles_statement)
  genres_statement_string = ", ".join(genres_statement)

  return execution, update, consoles_statement_string, genres_statement_string, consoles_update, genres_update

def validation(body):
  
  information = {}

  game_to_id, id_to_game = list_of_available_games()

  if "name" in body.keys():

    name_is_correct_format = isinstance(body["name"], str)

    if name_is_correct_format:

      if len(body["name"]) > 0:

        information["name"] = body["name"]

  if "own_status" in body.keys():

    own_status_to_id, id_to_own_status = list_of_available_own_statuses()
    own_status_is_correct_format = isinstance(body["own_status"], str)

    if own_status_is_correct_format:

      if len(body["own_status"]) > 0:
      
        own_status = body["own_status"].capitalize()
    
        if own_status in own_status_to_id.keys():

          information["own_status"] = own_status_to_id[own_status]

  if "played_status" in body.keys():

    played_status_to_id, id_to_played_status = list_of_available_played_statuses()
    played_status_is_correct_format = isinstance(body["played_status"], str)

    if played_status_is_correct_format:

      if len(body["played_status"]) > 0:
      
        played_status = body["played_status"].capitalize()

        if played_status in played_status_to_id.keys():

          information["played_status"] = played_status_to_id[played_status]

  if "genres" in body.keys():

    genre_to_id, id_to_genre = list_of_available_genres()
    genres_is_correct_format = isinstance(body["genres"], list)

    if genres_is_correct_format:

      if len(body["genres"]) > 0:
      
        genre_ids = []

        for genre in body["genres"]:

          genre_is_string = isinstance(genre, str)
          
          if genre_is_string:
            
            genre = genre.strip().capitalize()

            if genre in genre_to_id.keys(): 
            
              genre_ids.append(genre_to_id[genre])

    information["genres"] = genre_ids
  
  if "consoles" in body.keys():

    console_to_id, id_to_console, slug_to_id, id_to_slug = list_of_available_consoles()
    consoles_is_correct_format = isinstance(body["consoles"], list)

    if consoles_is_correct_format:

      if len(body["consoles"]) > 0:
      
        console_ids = []
        available_consoles = {key.lower() : value for key, value in console_to_id.items()}
        available_slug_consoles = {key.lower() : value for key, value in slug_to_id.items()}
        
        for console in body["consoles"]:
          
          console_is_string = isinstance(console, str)

          if console_is_string:

            console = console.strip().lower()

            if console in available_consoles.keys(): 

              console_ids.append(available_consoles[console])
            
            elif console in available_slug_consoles.keys():

              console_ids.append(available_slug_consoles[console])
    
    information["consoles"] = console_ids
  
  return information