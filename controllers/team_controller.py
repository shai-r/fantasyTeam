from dataclasses import asdict
from toolz import *
from flask import Blueprint, jsonify, request
from typing import List
from dto.CreateTeamDto import CreateTeamDto
from dto.ResponseDto import ResponseDto
from dto.TeamDto import TeamDto
from dto.UpdateTeamDto import UpdateTeamDto
from models.TeamPlayers import TeamPlayers
from repository.team_repository import delete_team
from service.team_service import create_team, convert_from_team_id_to_team_dto, update_team, get_all_teams_compare

teams_blueprint = Blueprint("teams", __name__)

@teams_blueprint.route('/', methods=['POST'])
def add_team():
    team = CreateTeamDto(**request.json)
    team = create_team(team)
    return jsonify(asdict(ResponseDto(body=team))), 201

@teams_blueprint.route("/<int:team_id>", methods=['GET'])
def team_by_id(team_id):
    team = convert_from_team_id_to_team_dto(team_id)
    return ((jsonify(asdict(ResponseDto(body=team))), 200) if team else
            (jsonify(asdict(ResponseDto(error='not found'))), 404))

@teams_blueprint.route("/<int:team_id>", methods=['DELETE'])
def delete(team_id):
    is_deleted = delete_team(team_id)
    return (jsonify(asdict(ResponseDto(message=is_deleted))), 200) if is_deleted else(
        (jsonify(asdict(ResponseDto(message='not found'))), 404))

@teams_blueprint.route("/<int:team_id>", methods=['PUT'])
def update(team_id):
    update = update_team(team_id, UpdateTeamDto(**request.json))
    return ((jsonify(asdict(ResponseDto(body=update))), 201) if update else
            (jsonify(asdict(ResponseDto(error='not found'))), 404))

@teams_blueprint.route("/compare", methods=['GET'])
def compare():
    args = request.args
    teams = [v for k, v in args.items() if k.startswith("team")]
    team_ids = list(map(lambda tid: int(tid),teams))
    teams_compare = get_all_teams_compare(team_ids)
    return ((jsonify(asdict(ResponseDto(body=teams_compare))), 200) if teams_compare else
            (jsonify(asdict(ResponseDto(error='not found'))), 404))