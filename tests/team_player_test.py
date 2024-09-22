import pytest
from repository.database import create_all_tables, drop_all_tables
from repository.team_players_repository import *
from service.player_service import load_players_and_seasons_from_api
from models.TeamPlayers import TeamPlayers

@pytest.fixture(scope="module")
def setup_database():
    create_all_tables()
    load_players_and_seasons_from_api(2024)
    # yield
    # drop_all_tables()

def test_create_team_player(setup_database):
    new_id = create_team_player_if_not_exists_else_find_id(TeamPlayers(team_id=1, player_id=3, position='C'))
    assert new_id >=1

def test_get_all_team_player(setup_database):
    team_players = get_all_team_players()
    assert team_players

def test_get_all_team_players_by_team_id(setup_database):
    team_players =get_all_team_players_by_team_id(1)
    assert team_players

def test_get_all_team_players_by_player_id(setup_database):
    team_players = get_all_team_players_by_player_id(1)
    assert team_players

def test_get_team_player_by_id(setup_database):
    team_players = get_team_player_by_id(2)
    assert team_players.id == 1

def test_update_team_player(setup_database):
    update_team_player(1, TeamPlayers(team_id=1, player_id=9, position='C'))
    team_player = get_team_player_by_id(1)
    assert team_player.player_id == 9

def test_delete_team(setup_database):
    assert delete_team_player(1)

def test_delete_team_player_by_team_id(setup_database):
    assert delete_team_player_by_team_id(1)

def test_delete_team_player_by_player_id(setup_database):
    assert delete_team_player_by_player_id(1)