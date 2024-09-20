from dataclasses import asdict
from flask import Blueprint, jsonify, request
from dto.ResponseDto import ResponseDto
from service.player_service import convert_players_to_player_dto_for_players_endpoint

players_blueprint = Blueprint("players", __name__)

@players_blueprint.route("/", methods=['GET'])
def all_players_in_position():
    args = request.args
    position = args['position']
    season = args['season'] if 'season' in args.keys()  else 0
    return jsonify(asdict(ResponseDto(body=convert_players_to_player_dto_for_players_endpoint(position, season)))), 200
