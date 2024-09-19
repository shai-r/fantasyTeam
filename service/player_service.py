from toolz import groupby, curry
from toolz.curried import reduce
from typing import List
from api.data_api import get_data
from dto.PlayerDto import PlayerDto
from models.Player import Player
from models.PlayerSeason import PlayerSeason
from repository import get_player_by_id
from repository.player_repository import get_all_players, create_player_if_not_exists_else_find_id
from repository.player_season_repository import create_player_season_if_not_exists, get_all_player_seasons, \
    get_player_season_by_id
from toolz import map, filter, pipe, partial
import statistics as s

def load_players_and_seasons_from_api(season: int):
        if get_all_players() is None or len(get_all_players()) < 5:
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

def reduce_list_of_players(points_per_games: float, seasons: List[PlayerSeason]):
    return PlayerDto(
        playerName=seasons[0].playerName,
        team=seasons[0].team,
        position=seasons[0].position,
        season=list(map(lambda s: s.season, seasons)),
        points=sum(map(lambda s: s.points, seasons)),
        games=sum(map(lambda s: s.games, seasons)),
        twoPercent=s.mean(map(lambda s: s.twoPercent, seasons)),
        threePercent=s.mean(map(lambda s: s.threePercent, seasons)),
        ATR=s.mean(map(lambda s: s.ATR, seasons)),
        PPG=s.mean(map(lambda s: s.PPG, seasons))/points_per_games,
        )

def convert_player_to_player_dto(position: str, season: int):
    data = get_all_player_seasons()

    in_position =  pipe(
        data,
        partial(filter, lambda p: position in p.position),
        partial(filter, lambda p: p.season == season if season in [2022, 2023, 2024] else True),
        list
        )

    all_games = s.mean(map(lambda p: p.games, data))
    all_points = s.mean(map(lambda p: p.points, data))
    points_per_games = all_points / all_games

    return pipe(
        in_position,
        partial(map, lambda p: PlayerDto(
            playerName=get_player_by_id(p.player_id).player_name,
            team=p.team,
            position=p.position,
            season=p.season,
            points=p.points,
            games=p.games,
            twoPercent=p.two_percent,
            threePercent=p.three_percent,
            ATR=p.atr,
            PPG=p.points/p.games,
        )),
        partial(lambda li: groupby(key=lambda p: p.playerName, seq=li).values()),
        partial(map, partial(reduce_list_of_players, points_per_games)),
        list
    )