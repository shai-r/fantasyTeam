from typing import List
from api.data_api import get_data
from dto.PlayerDto import PlayerDto
from models.Player import Player
from models.PlayerSeason import PlayerSeason
from repository import get_player_by_id
from repository.player_repository import get_all_players, create_player_if_not_exists_else_find_id
from repository.player_season_repository import create_player_season_if_not_exists, get_all_player_seasons
from toolz import map, filter, pipe, partial, groupby
import statistics as s

def load_players_and_seasons_from_api(season: int):
        if get_all_players() is None or len(get_all_players()) < 20:
            players = get_data(
                f'http://b8c40s8.143.198.70.30.sslip.io/api/PlayerDataTotals/query?season={season}&&pageSize=1000')
            for p in players:
                pid = create_player_if_not_exists_else_find_id(
                    Player(api_id=p['playerId'], player_name=p['playerName']))
                create_player_season_if_not_exists(
                    PlayerSeason(
                        player_id=pid,
                        team=p['team'],
                        position=p['position'],
                        season=p['season'],
                        points=p['points'] or 0,
                        games=p['games'] or 0,
                        two_percent=p['twoPercent'] or 0,
                        three_percent=p['threePercent'] or 0 ,
                        atr=p['assists'] if p['turnovers'] == 0 else p['assists'] / p['turnovers']
                    )
                )

def reduce_list_of_players(seasons: List[PlayerSeason]):
    return PlayerDto(
        player_id=seasons[0].player_id,
        playerName=seasons[0].playerName,
        team=seasons[0].team,
        position=seasons[0].position,
        season=list(map(lambda s: s.season, seasons)),
        points=sum(map(lambda s: s.points, seasons)),
        games=sum(map(lambda s: s.games, seasons)),
        twoPercent=s.mean(map(lambda s: s.twoPercent, seasons)),
        threePercent=s.mean(map(lambda s: s.threePercent, seasons)),
        ATR=s.mean(map(lambda s: s.ATR, seasons)),
        PPG=s.mean(map(lambda s: s.PPG, seasons)),
        )

def get_all_players_in_position_and_in_season(position: str, season: int):
    return pipe(
        get_all_player_seasons(),
        partial(filter, lambda p: position in p.position),
        partial(filter, lambda p: p.season == season if season in [2022, 2023, 2024] else True),
        list
    )

def get_all_points_per_games(position: str, season: int):
    data = get_all_players_in_position_and_in_season(position, season)
    all_games = s.mean(map(lambda p: p.games, data))
    all_points = s.mean(map(lambda p: p.points, data))
    return all_points / all_games

def convert_players_to_player_dto_for_players_endpoint(position: str, season: int) -> List[PlayerDto]:
    return pipe(
        get_all_players_in_position_and_in_season(position, season),
        partial(map, lambda p: PlayerDto(
            player_id=p.player_id,
            playerName=get_player_by_id(p.player_id).player_name,
            team=p.team,
            position=p.position,
            season=p.season,
            points=p.points,
            games=p.games,
            twoPercent=p.two_percent,
            threePercent=p.three_percent,
            ATR=p.atr,
            PPG=(p.points/p.games)/ get_all_points_per_games(position,season),
        )),
        partial(lambda li: groupby(key=lambda p: p.playerName, seq=li).values()),
        partial(map, partial(reduce_list_of_players)),
        list
    )

def convert_player_to_player_dto(player: PlayerSeason):
    return PlayerDto(
        player_id=player.player_id,
        playerName=get_player_by_id(player.player_id).player_name,
        team=player.team,
        position=player.position,
        season=player.season,
        points=player.points,
        games=player.games,
        twoPercent=player.two_percent,
        threePercent=player.three_percent,
        ATR=player.atr,
        PPG=(player.points / player.games) / get_all_points_per_games(player.position, player.season)
    )