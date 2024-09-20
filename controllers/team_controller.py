from dataclasses import asdict
from toolz import *
from flask import Blueprint, jsonify, request

from dto.CreateTeamDto import CreateTeamDto
from dto.ResponseDto import ResponseDto
from dto.TeamDto import TeamDto
from service.team_service import create_team, convert_from_team_id_to_team_dto

teams_blueprint = Blueprint("teams", __name__)

@teams_blueprint.route('/', methods=['POST'])
def add_team():
    breakpoint()
    team = CreateTeamDto(**request.json)
    breakpoint()
    team = create_team(team)
    return jsonify(asdict(ResponseDto(body=team))), 201

@teams_blueprint.route("/<int:team_id>", methods=['GET'])
def team_by_id(team_id):
    team = convert_from_team_id_to_team_dto(team_id)
    return ((jsonify(asdict(ResponseDto(body=team))), 200) if team else
            (jsonify(asdict(ResponseDto(error='not found'))), 404))
# @teams_blueprint.route("/", methods=['GET'])
# def all_teams():
#     args = request.args
#     position = args['position']
#     season = args['season'] if 'season' in args.keys()  else 0
#     return jsonify(asdict(ResponseDto(body=convert_player_to_player_dto('C', 0)))), 200

#
#

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