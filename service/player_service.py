from api.data_api import get_data
from models.Player import Player
from models.PlayerSeason import PlayerSeason
from repository.player_repository import get_all_players, create_player_if_not_exists_else_find_id
from repository.player_season_repository import create_player_season_if_not_exists

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


