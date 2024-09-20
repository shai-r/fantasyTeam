from functools import partial
from typing import List, Optional

from toolz import first, pipe
from dto.TeamDto import TeamDto
from dto.CreateTeamDto import CreateTeamDto
from models.Team import Team
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
def create_team(team: CreateTeamDto) -> Optional[TeamDto]:
    # players = set(players)
    players_positions = list(map(lambda player: player.position, team.players))
    if len(team.players) < 5 or not all(map(lambda p: p in players_positions, positions)):
        return None

    seasons: List[int] = list(map(lambda player: get_player_season_by_id(player.player_id).season, players))

    if any(season != seasons[0] for season in seasons):
        return None

    new_team_id = create_team_if_not_exists_else_find_id(
        Team(team_name=team.team_name, season=first(seasons))
    )

    for player in team.players:
        if player.player_id not in map(lambda p: p.id, get_all_team_players_by_team_id(new_team_id)):
            player.team_id = new_team_id
            create_team_player_if_not_exists_else_find_id(player)

    return convert_from_team_id_to_team_dto(new_team_id)

