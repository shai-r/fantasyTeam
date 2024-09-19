from dataclasses import asdict
from toolz import *
from flask import Blueprint, jsonify, request
from dto.ResponseDto import ResponseDto
from models.Player import Player
from models.PlayerSeason import PlayerSeason
from repository.player_repository import *
from repository.player_season_repository import get_all_player_seasons
from service.player_service import convert_player_to_player_dto

players_blueprint = Blueprint("players", __name__)

@players_blueprint.route("/", methods=['GET'])
def all_users():
    args = request.args
    position = args['position']
    season = args['season'] if 'season' in args.keys()  else 0
    return jsonify(asdict(ResponseDto(body=convert_player_to_player_dto('C', 0)))), 200

# @user_blueprint.route("/create", methods=['POST'])
# def add_user():
#     user = User(**request.json)
#     uid = create_user(user)
#     user.id = uid
#     return jsonify(asdict(ResponseDto(body=user))), 201
#
# @user_blueprint.route("/<int:user_id>", methods=['GET'])
# def user_by_id(user_id):
#     user = get_user_by_id(user_id)
#     return ((jsonify(asdict(ResponseDto(body=user))), 200) if user else
#             (jsonify(asdict(ResponseDto(error='not found'))), 404))
#
# @user_blueprint.route("/update/<int:user_id>", methods=['PUT'])
# def update(user_id):
#     user = update_user(user_id, User(**request.json))
#     return ((jsonify(asdict(ResponseDto(body=user))), 201) if user else
#             (jsonify(asdict(ResponseDto(error='not found'))), 404))
#
# @user_blueprint.route("/delete/<int:user_id>", methods=['DELETE'])
# def delete(user_id):
#     is_deleted = delete_user(user_id)
#     return jsonify(asdict(ResponseDto(message=is_deleted))), 200 if is_deleted else 404