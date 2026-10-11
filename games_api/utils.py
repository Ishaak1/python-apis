import sqlite3
from flask import jsonify

def concat_genres_consoles(games):
  
  game_details_together = []

  if len(games) > 0:

    name = games[0]["name"]
    genres = []
    consoles = []
    game_details = {"name": games[0]["name"], "id": games[0]["id"], "own_status": games[0]["own_status"], "played_status": games[0]["played_status"] }

    for i in range(len(games)):
      
      if name != games[i]["name"]:

        game_details["genres"] = genres
        game_details["consoles"] = consoles
        game_details_together.append(game_details)
        game_details = {}
        name = games[i]["name"]
        info_id = games[i]["id"]
        own_status = games[i]["own_status"]
        played_status = games[i]["played_status"]
        game_details["id"] = info_id
        game_details["own_status"] = own_status
        game_details["name"] = name
        game_details["played_status"] = played_status
        genres = []
        consoles = []

      if games[i]["genre"] not in genres:
        
        genres.append(games[i]["genre"])
      
      console = f"{games[i]["console"]} ({games[i]["company"]})"
      
      if console not in consoles:
        
        consoles.append(console)

      if i == len(games) - 1:
        
        game_details["genres"] = genres
        game_details["consoles"] = consoles
        game_details_together.append(game_details)
    
  return game_details_together

def list_of_available_games():
  
  db = sqlite3.connect("games.db")
  db.row_factory = sqlite3.Row
  cursor = db.cursor()
  
  cursor.execute("SELECT * FROM games")
  games = [dict(game) for game in cursor.fetchall()]
  game_to_id = {game["name"] : game["id"] for game in games}
  id_to_game = {game["id"] : game["name"] for game in games}

  return game_to_id, id_to_game

def list_of_available_own_statuses():

  db = sqlite3.connect("games.db")
  db.row_factory = sqlite3.Row
  cursor = db.cursor()
  
  cursor.execute("SELECT * FROM own_statuses")
  own_statuses = [dict(own_status) for own_status in cursor.fetchall()]
  own_status_to_id = {own_status["own_status"]: own_status["id"] for own_status in own_statuses}
  id_to_own_status = {own_status["id"]: own_status["own_status"] for own_status in own_statuses}

  return own_status_to_id, id_to_own_status

def list_of_available_consoles():

  db = sqlite3.connect("games.db")
  db.row_factory = sqlite3.Row
  cursor = db.cursor()

  cursor.execute("SELECT * FROM consoles")
  consoles = [dict(console) for console in cursor.fetchall()]
  console_to_id = {console["console"] : console["id"] for console in consoles}
  id_to_console = {console["id"] : console["console"] for console in consoles}
  slug_to_id = {console["slug"] : console["id"] for console in consoles}
  id_to_slug = {console["id"] : console["slug"] for console in consoles}
  
  return console_to_id, id_to_console, slug_to_id, id_to_slug

def list_of_available_genres():

  db = sqlite3.connect("games.db")
  db.row_factory = sqlite3.Row
  cursor = db.cursor()
  
  cursor.execute("SELECT * FROM genres")
  genres = [dict(genre) for genre in cursor.fetchall()]
  genre_to_id = {genre["genre"] : genre["id"] for genre in genres}
  id_to_genre = {genre["id"] : genre["genre"] for genre in genres}

  return genre_to_id, id_to_genre

def list_of_available_played_statuses():
  
  db = sqlite3.connect("games.db")
  db.row_factory = sqlite3.Row
  cursor = db.cursor()
  
  cursor.execute("SELECT * FROM played_statuses")
  played_statuses = [dict(played_status) for played_status in cursor.fetchall()]
  played_status_to_id = {played_status["played_status"] : played_status["id"] for played_status in played_statuses}
  id_to_played_status = {played_status["id"] : played_status["played_status"] for played_status in played_statuses}

  return played_status_to_id, id_to_played_status

def validation_for_adding_game(body):

  correct_keys = ["name", "own_status", "played_status", "genres", "consoles"]
  inserted_keys = []
  information = {}

  for key, value in body.items():

    if key not in correct_keys:

      return {}

    inserted_keys.append(key)

  game_to_id, id_to_game = list_of_available_games()

  name = body["name"].strip()

  if name not in game_to_id.keys() and len(name) > 0:

    correct_name_format = isinstance(name, str)

    if not correct_name_format:

      return {}

    else:

      information["name"] = name

    if "played_status" in inserted_keys:

      correct_played_status_format = isinstance(body["played_status"], str)

      if correct_played_status_format:

        played_status_to_id, id_to_played_status = list_of_available_played_statuses()
        played_status = body["played_status"].capitalize()

        if played_status in played_status_to_id.keys():
          
          played_status_id = played_status_to_id[played_status]
          information["played_status"] = played_status_id

        else:

          return {}
      
      else: 

        return {}

    else:

      played_status_id = 1
      information["played_status"] = played_status_id
    
    if "own_status" in inserted_keys:

      correct_own_status_format = isinstance(body["own_status"], str)

      if correct_own_status_format:

        own_status_to_id, id_to_own_status = list_of_available_own_statuses()
        own_status = body["own_status"].capitalize()

        if own_status in own_status_to_id.keys():

          own_status_id = own_status_to_id[own_status]
          information["own_status"] = own_status_id
       
        else:

          return {}      
      
      else: 

        db.close()

        return {}

    else:

      own_status_id = 1
      information["own_status"] = own_status_id

    genres_is_a_list = isinstance(body["genres"], list)
    genre_ids = []

    if genres_is_a_list:

      for genre in body["genres"]:

        is_correct_format = isinstance(genre, str)

        if is_correct_format:
          
          genre = genre.strip().title()
          genre_to_id, id_to_genre = list_of_available_genres()

          if genre in genre_to_id.keys():
            
            genre_ids.append(genre_to_id[genre])

          else: 
            
            return {}
    
      information["genres"] = genre_ids

    else: 

      return {}

    consoles_is_a_list = isinstance(body["consoles"], list)
    console_ids = []

    if consoles_is_a_list:

      for console in body["consoles"]:
        
        console = console.strip().lower()
        is_correct_format = isinstance(console, str)

        if is_correct_format:

          console_to_id, id_to_console, slug_to_id, id_to_slug = list_of_available_consoles()
          available_consoles = {key.lower() : value for key, value in console_to_id.items()}
          available_slug_consoles = {key.lower() : value for key, value in slug_to_id.items()}

          if console in available_consoles.keys():

            console_ids.append(available_consoles[console])

          elif console in available_slug_consoles.keys():

            console_ids.append(slug_to_id[console])

        else:            
          
          return {}

      information["consoles"] = console_ids

  else: 
  
    return {}

  return information

def create_game_statement(information):

  keys = []
  update = []
  
  for key, value in information.items():
    
    if key == "name":

      keys.append("(?, ?, ?)")
      update.append(value)

    elif key == "played_status":

      update.append(value)

    elif key == "own_status":

      update.append(value)

  return keys, update

def create_console_genre_statement(information, name_to_id):

  consoles_statement = []
  genres_statement = []
  consoles_update = []
  genres_update = []
  game_id = name_to_id[information["name"]]
  
  for key, value in information.items():

    if key == "consoles":

      for item in value:

        consoles_statement.append("(?, ?)")
        consoles_update.append(game_id)
        consoles_update.append(item)

    elif key == "genres":

      for item in value:
        
        genres_statement.append("(?, ?)")
        genres_update.append(game_id)
        genres_update.append(item)

  return consoles_statement, genres_statement, consoles_update, genres_update