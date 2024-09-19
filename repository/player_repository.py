from models.Player import Player
from repository.database import get_db_connection, create_players_table
from typing import List, Optional

from repository import delete_player_season_by_player_id

def get_player_by_api_id(a_id: str) -> Optional[Player]:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT * FROM players WHERE api_id = %s", (a_id,))
        player = cursor.fetchone()
        return None if not player else Player(**player)

def create_player_if_not_exists_else_find_id(player: Player) -> int:
    player_exists = get_player_by_api_id(player.api_id)
    if player_exists:
        return player_exists.id

    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO players (api_id, player_name)
            VALUES (%s, %s) RETURNING id
        """, (player.api_id, player.player_name))
        new_id = cursor.fetchone()['id']
        connection.commit()
        return new_id

def get_all_players():
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT * FROM players")
        res = cursor.fetchall()
        player = [Player(**p) for p in res]
        return player if player else None


def get_player_by_id(pid: int) -> Optional[Player]:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT * FROM players WHERE id = %s", (pid,))
        player = cursor.fetchone()
        return None if not player else Player(**player)


def update_player(pid: int, player: Player) -> Player:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute(
            "UPDATE players SET api_id = %s, player_name = %s",
            (player.api_id, player.player_name)
        )
        connection.commit()
        player = get_player_by_id(pid)
        return player

def delete_player(pid: int):
    if get_player_by_id(pid) == None:
        return False
    delete_player_season_by_player_id(pid)
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("DELETE FROM players WHERE id = %s", (pid,))
        connection.commit()
        return get_player_by_id(pid) == None

