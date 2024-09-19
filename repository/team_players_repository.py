from models.TeamPlayers import TeamPlayers
from repository.database import get_db_connection
from typing import List, Optional

def is_team_players_exists(team_player: TeamPlayers) -> Optional[TeamPlayers]:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM team_players WHERE team_id = %s AND player_id = %s",
            (team_player.team_id, team_player.player_id)
        )
        player = cursor.fetchone()
        return None if not player else TeamPlayers(**player)

def create_team_player_if_not_exists_else_find_id(team_player: TeamPlayers) -> int:
    player_exists = is_team_players_exists(team_player)
    if player_exists:
        return player_exists.id

    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO team_players (team_id, player_id, position)
            VALUES (%s, %s, %s) RETURNING id
        """, (team_player.team_id, team_player.player_id, team_player.position))
        new_id = cursor.fetchone()['id']
        connection.commit()
        return new_id

def get_all_team_players() -> List[TeamPlayers]:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT * FROM team_players")
        res = cursor.fetchall()
        team_players = [TeamPlayers(**tp) for tp in res]
        return team_players if team_players else []

def get_all_team_players_by_team_id(tid) ->List[TeamPlayers]:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT * FROM team_players WHERE team_id = %s", (tid,))
        res = cursor.fetchall()
        team_players = [TeamPlayers(**tp) for tp in res]
        return team_players if team_players else []

def get_all_team_players_by_player_id(pid) ->List[TeamPlayers]:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT * FROM team_players WHERE player_id = %s", (pid,))
        res = cursor.fetchall()
        team_players = [TeamPlayers(**tp) for tp in res]
        return team_players if team_players else []

def get_team_player_by_id(t_p_id: int) -> Optional[TeamPlayers]:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT * FROM team_players WHERE id = %s", (t_p_id,))
        team_player = cursor.fetchone()
        return None if not team_player else TeamPlayers(**team_player)


def update_team_player(t_p_id: int, team_player: TeamPlayers) -> TeamPlayers:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute(
            "UPDATE team_players SET team_id = %s, player_id = %s, position = %s",
            (team_player.team_id, team_player.player_id, team_player.position)
        )
        connection.commit()
        team_player = get_team_player_by_id(t_p_id)
        return team_player

def delete_team_player(pid: int):
    if get_team_player_by_id(pid) == None:
        return False
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("DELETE FROM team_players WHERE id = %s", (pid,))
        connection.commit()
        return get_team_player_by_id(pid) == None

def delete_team_player_by_team_id(tid: int):
    if get_all_team_players_by_team_id(tid) == None:
        return False
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("DELETE FROM team_players WHERE team_id = %s", (tid,))
        connection.commit()
        return get_all_team_players_by_team_id(tid) == None

def delete_team_player_by_player_id(pid: int):
    if get_all_team_players_by_player_id(pid) == None:
        return False
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("DELETE FROM team_players WHERE player_id = %s", (pid,))
        connection.commit()
        return get_all_team_players_by_player_id(pid) == None

