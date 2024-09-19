from toolz import pipe, first
from toolz.curried import partial

from models.PlayerSeason import PlayerSeason
from repository.database import get_db_connection
from typing import List, Optional

from repository.team_players_repository import delete_team_player_by_player_id


def create_player_season_if_not_exists(player_season: PlayerSeason) -> int:
    player_s = pipe(
        get_all_player_season_by_player_id(player_season.player_id),
        partial(filter, lambda p: p.season == player_season.season),
        lambda li: next(li, None)
    )

    if player_s:
        return player_s.id

    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO player_seasons (player_id, team, position, season, points, 
            games, two_percent, three_percent, atr)
            VALUES (%s, %s , %s, %s, %s, %s, %s, %s, %s) RETURNING id
        """, (player_season.player_id, player_season.team, player_season.position,
              player_season.season, player_season.points, player_season.games,
              player_season.two_percent, player_season.three_percent,
              player_season.atr))
        new_id = cursor.fetchone()['id']
        connection.commit()
        return new_id


def get_all_player_seasons() -> List[PlayerSeason]:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT * FROM player_seasons")
        res = cursor.fetchall()
        player_seasons = [PlayerSeason(**p) for p in res]
        return player_seasons if player_seasons else None


def get_all_player_season_by_player_id(pid: int) -> List[PlayerSeason]:
    from repository import get_player_by_id

    if get_player_by_id(pid) is None:
        return []

    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT * FROM player_seasons WHERE player_id = %s", (pid,))
        res = cursor.fetchall()
        player_seasons = [PlayerSeason(**p) for p in res]
        return player_seasons


def get_player_season_by_id(psid: int) -> Optional[PlayerSeason]:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT * FROM player_seasons WHERE id = %s", (psid,))
        player_season = cursor.fetchone()
        return None if not player_season else PlayerSeason(**player_season)


def update_player_season(psid: int, player_season: PlayerSeason) -> PlayerSeason:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute(
            "UPDATE player_seasons SET player_id = %s, team = %s, "
            "position = %s, season = %s, points = %s, games = %s, two_percent = %s, "
            "three_percent = %s , atr = %s)",
            (player_season.player_id, player_season.team, player_season.position,
             player_season.season, player_season.points, player_season.games,
             player_season.two_percent, player_season.three_percent,
             player_season.atr)
        )
        connection.commit()
        player_season = get_player_season_by_id(psid)
        return player_season


def delete_player_season(psid: int):
    if get_player_season_by_id(psid) == None:
        return False
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("DELETE FROM player_seasons WHERE id = %s", (psid,))
        connection.commit()
        return get_player_season_by_id(psid) == None


def delete_player_season_by_player_id(pid: int):
    delete_team_player_by_player_id(pid)
    from repository import get_player_by_id

    if get_player_by_id(pid) == None:
        return False
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("DELETE FROM player_seasons WHERE player_id = %s", (pid,))
        connection.commit()
        return get_player_season_by_id(pid) == None
