import sqlite3
from flask import Flask, request, jsonify
from config import seed_db
from fetch_all_games import fetch_games_bp
from fetch_game import fetch_game_bp
from fetch_by_played_status import fetch_by_played_status_bp
from fetch_by_own_status import fetch_by_own_status_bp
from fetch_by_genre import fetch_by_genre_bp
from fetch_by_console import fetch_by_console_bp
from delete_game import delete_game_bp
from delete_by_own_status import delete_by_own_status_bp
from delete_by_played_status import delete_by_played_status_bp
from update_played_status import update_played_status_bp
from update_own_status import update_own_status_bp
from update_name import update_name_bp
from update_game import update_game_bp
from add_game import add_game_bp
from add_games import add_games_bp

app = Flask(__name__)

app.register_blueprint(fetch_games_bp)
app.register_blueprint(fetch_game_bp)
app.register_blueprint(fetch_by_played_status_bp)
app.register_blueprint(fetch_by_own_status_bp)
app.register_blueprint(fetch_by_genre_bp)
app.register_blueprint(fetch_by_console_bp)
app.register_blueprint(delete_game_bp)
app.register_blueprint(delete_by_own_status_bp)
app.register_blueprint(delete_by_played_status_bp)
app.register_blueprint(update_played_status_bp)
app.register_blueprint(update_own_status_bp)
app.register_blueprint(update_name_bp)
app.register_blueprint(update_game_bp)
app.register_blueprint(add_game_bp)
app.register_blueprint(add_games_bp)

@app.route("/")
def home():
  return "API is running on port 5000", 200

if __name__ == "__main__":

  db = sqlite3.connect("games.db")
  cursor = db.cursor()
  seed_db(db, cursor)
  app.run(debug=True)
  db.close()

# CREATE:
# add_game = "/game"
# add_games = "/games"

# DELETE:
# delete_game = "/game/<int:remove>"
# delete_by_own_status = "/games/ownership/<string:status>"
# delete_by_played_status = "/games/played/<string:status>"

# UPDATE:
# update_game = "/game/<int:game_id>"
# update_name = "/game/name/<int:id>"
# update_game_own_status = "/game/ownership/<int:id>/<string:status>"
# update_played_status = "/game/played/<int:id>/<string:status>"

# READ:
# get_game = "/game/<int:id>"
# get_all_games = "/games"
# get_by_console = "/games/platform/<string:console>"
# get_by_genre = "/games/genre/<string:genre>"
# get_by_own_status = "/games/ownership/<string:status>"
# get_by_played_status = "/games/played/<string:status>"