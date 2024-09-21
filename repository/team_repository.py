from models.Team import Team
from models.Team import Team
from repository.database import get_db_connection
from typing import List, Optional

from repository.team_players_repository import delete_team_player_by_team_id


def is_team_exists(team: Team) -> Optional[Team]:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT * FROM teams WHERE team_name = %s",(team.team_name,))
        team = cursor.fetchone()
        return None if not team else Team(**team)


def create_team_if_not_exists_else_find_id(team: Team) -> int:
    player_exists = is_team_exists(team)
    if player_exists:
        return player_exists.id

    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO teams (team_name, season)
            VALUES (%s, %s) RETURNING id
        """, (team.team_name, team.season))
        new_id = cursor.fetchone()['id']
        connection.commit()
        return new_id


def get_all_team() -> List[Team]:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT * FROM teams")
        res = cursor.fetchall()
        teams = [Team(**t) for t in res]
        return teams if teams else []

def get_team_by_id(tid: int) -> Optional[Team]:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT * FROM teams WHERE id = %s", (tid,))
        team = cursor.fetchone()
        return None if not team else Team(**team)


def update_team(tid: int, team: Team) -> Team:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute(
            "UPDATE teams SET team_name = %s, season = %s",
            (team.team_name, team.season)
        )
        connection.commit()
        team = get_team_by_id(tid)
        return team


def delete_team(tid: int):
    delete_team_player_by_team_id(tid)
    if get_team_by_id(tid) == None:
        return None
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("DELETE FROM teams WHERE id = %s", (tid,))
        connection.commit()
        return get_team_by_id(tid) == None