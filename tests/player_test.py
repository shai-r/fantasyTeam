import pytest
from repository.database import create_all_tables, drop_all_tables
from repository.player_repository import *
from service.player_service import load_players_and_seasons_from_api
from models.Player import Player

@pytest.fixture(scope="module")
def setup_database():
    create_all_tables()
    load_players_and_seasons_from_api(2022)
    # yield
    # drop_all_tables()

def test_create_player(setup_database):
    new_id = create_player_if_not_exists_else_find_id(Player(api_id='Shai01', player_name='Shai'))
    assert new_id >=1

def test_get_all_players(setup_database):
    players = get_all_players()
    assert players

def test_get_player_by_id(setup_database):
    players = get_player_by_id(6)
    assert players.id == 6

def test_update_player(setup_database):
    update_player(6, Player(api_id='Shaios', player_name="Shai"))
    players = get_player_by_id(6)
    assert players.api_id == 'Shaios'

def test_delete_player(setup_database):
    assert delete_player(6)
