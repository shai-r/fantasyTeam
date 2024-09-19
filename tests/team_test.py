import pytest
from repository.database import create_all_tables, drop_all_tables
from repository.team_repository import *
from service.player_service import load_players_and_seasons_from_api
from models.Team import Team

@pytest.fixture(scope="module")
def setup_database():
    create_all_tables()
    load_players_and_seasons_from_api(2024)
    # yield
    # drop_all_tables()

def test_create_team(setup_database):
    new_id = create_team_if_not_exists_else_find_id(Team(team_name='Shai01', season=2025))
    assert new_id >=1

def test_get_all_teams(setup_database):
    teams = get_all_team()
    assert teams

def test_get_team_by_id(setup_database):
    team = get_team_by_id(1)
    assert team.id == 1

def test_update_team(setup_database):
    update_team(1, Team(team_name='Shaios', season=205))
    team = get_team_by_id(1)
    assert team.team_name == 'Shaios'

def test_delete_team(setup_database):
    assert delete_team(1)
