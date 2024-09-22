from functools import partial
from typing import List, Optional
import statistics as s
from toolz import first, pipe
from dto.TeamDto import TeamDto
from dto.CreateTeamDto import CreateTeamDto
from dto.Team_Compare import TeamCompare
from dto.UpdateTeamDto import UpdateTeamDto
from models.PlayerSeason import PlayerSeason
from models.Team import Team
from models.TeamPlayers import TeamPlayers
from repository.player_season_repository import get_player_season_by_id
from repository.team_players_repository import create_team_player_if_not_exists_else_find_id, \
    get_all_team_players_by_team_id, get_all_team_players, delete_team_player_by_team_id
from repository.team_repository import create_team_if_not_exists_else_find_id, get_team_by_id, get_all_team
from service.player_service import convert_player_to_player_dto, get_all_points_per_games


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

def update_team(team_id: int, players_dto: UpdateTeamDto) -> Optional[bool]:
    players = set(players_dto.players)
    all_player_ids_in_teams = map(lambda p: p.player_id, get_all_team_players())
    players =  list(filter(lambda pid: pid not in all_player_ids_in_teams, players))

    players_positions: list[str] = list(map(lambda player_id: get_player_season_by_id(player_id).position, players))
    seasons: List[int] = list(map(lambda player_id: get_player_season_by_id(player_id).season, players))

    if len(players) < 5 or not all(map(lambda p: p in players_positions, positions)):
        return None


    if any(season != seasons[0] for season in seasons):
        return None

    delete_team_player_by_team_id(team_id)

    for player_id in players:
        if player_id not in map(lambda p: p.id, get_all_team_players_by_team_id(team_id)):
            create_team_player_if_not_exists_else_find_id(TeamPlayers(
                player_id=player_id,position=get_player_season_by_id(player_id).position, team_id=team_id))

    return True

def get_team_compare(team_id: int):
    name = get_team_by_id(team_id).team_name
    team_players = get_all_team_players_by_team_id(team_id)
    all_players = list(map(lambda p: get_player_season_by_id(p.player_id), team_players))
    # points = sum(map(lambda p: p.points, all_players)),
    # twoPercent = s.mean(list(map(lambda p: p.two_percent, all_players))) if len(all_players) > 0 else 0,
    # threePercent = s.mean(map(lambda p: p.three_percent, all_players)) if len(all_players) > 0 else 0,
    # ATR = s.mean(map(lambda p: p.atr, all_players)) or 0,
    # PPG = s.mean(map(lambda p: (p.points / p.games) / get_all_points_per_games(p.position, p.season), all_players)) or 0
    return TeamCompare(
        team=name,
        points=sum(map(lambda p: p.points, all_players)),
        twoPercent=s.mean(list(map(lambda p: p.two_percent, all_players))) if len(all_players) > 0 else 0,
        threePercent=s.mean(map(lambda p: p.three_percent, all_players)) if len(all_players) > 0 else 0,
        ATR=s.mean(map(lambda p: p.atr, all_players))if len(all_players) > 0 else 0,
        PPG=s.mean(map(lambda p: (p.points/ p.games)/ get_all_points_per_games(p.position,p.season), all_players))if len(all_players) > 0 else 0,
    )

def get_all_teams_compare(team_ids: List[int]):
    if len(team_ids) < 2:
        return None
    teams = list(map(lambda tid: get_team_compare(tid), team_ids))
    teams = sorted(teams, key=lambda t: t.PPG)
    return list(teams[::-1])

