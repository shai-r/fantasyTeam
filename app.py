from flask import Flask

from controllers.players_controller import *
from repository.database import create_all_tables
from service.player_service import load_players_and_seasons_from_api


app = Flask(__name__)

if __name__ == '__main__':
    create_all_tables()
    # load_players_and_seasons_from_api(2024)
    # load_players_and_seasons_from_api(2023)
    # load_players_and_seasons_from_api(2022)
    app.register_blueprint(players_blueprint, url_prefix="/api/players")
    app.run(debug=True)