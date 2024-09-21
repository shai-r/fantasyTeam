from functools import partial
from typing import List, Optional

from toolz import first, pipe
from dto.TeamDto import TeamDto
from dto.CreateTeamDto import CreateTeamDto
from models.Team import Team
from models.TeamPlayers import TeamPlayers
from repository.player_season_repository import get_player_season_by_id
from repository.team_players_repository import create_team_player_if_not_exists_else_find_id, \
    get_all_team_players_by_team_id
from repository.team_repository import create_team_if_not_exists_else_find_id, get_team_by_id
from service.player_service import convert_player_to_player_dto


def convert_from_team_id_to_team_dto(team_id: int) ->Optional[TeamDto]:
    team = get_team_by_id(team_id)
    all_players_in_team = get_all_team_players_by_team_id(team_id)
    players = pipe(
        all_players_in_team,
        partial(map, lambda p: (convert_player_to_player_dto(get_player_season_by_id(p.player_id)))),
        list
    )
    return TeamDto(
        team_id=team_id,
        team_name=team.team_name,
        players=players
    )


positions = ['PG', 'SG', 'SF', 'PF', 'C']
def create_team(team: CreateTeamDto) -> Optional[int]:
    team.players = set(team.players)
    players_positions: list[str] = list(map(lambda player_id: get_player_season_by_id(player_id).position, team.players))
    seasons: List[int] = list(map(lambda player_id: get_player_season_by_id(player_id).season, team.players))

    if len(team.players) < 5 or not all(map(lambda p: p in players_positions, positions)):
        return None


    if any(season != seasons[0] for season in seasons):
        return None

    new_team_id = create_team_if_not_exists_else_find_id(
        Team(team_name=team.team_name, season=first(seasons))
    )

    for player_id in team.players:
        if player_id not in map(lambda p: p.id, get_all_team_players_by_team_id(new_team_id)):
            create_team_player_if_not_exists_else_find_id(TeamPlayers(
                player_id=player_id,position=get_player_season_by_id(player_id).position, team_id=new_team_id))

    return new_team_id

