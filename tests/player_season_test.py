import pytest
from repository.database import create_all_tables, drop_all_tables
from repository.player_season_repository import *
from service.player_service import load_players_and_seasons_from_api
from models.PlayerSeason import PlayerSeason

@pytest.fixture(scope="module")
def setup_database():
    create_all_tables()
    load_players_and_seasons_from_api(2024)
    # yield
    # drop_all_tables()

def test_create_player(setup_database):
    new_id = create_player_season_if_not_exists(PlayerSeason(player_id=1,
                        team='kadachat',
                        position='C',
                        season=2025,
                        points=256,
                        games=32,
                        two_percent=.128,
                        three_percent=.256 ,
                        atr=.2))
    assert new_id >=21

def test_get_all_player_season(setup_database):
    player_seasons = get_all_player_seasons()
    assert player_seasons

def test_get_all_player_season_by_player_id(setup_database):
    player_seasons = get_all_player_season_by_player_id(5)
    assert player_seasons

def test_get_player_by_id(setup_database):
    player_season = get_player_season_by_id(3)
    assert player_season.id == 3

def test_update_player(setup_database):
    update_player_season(3, PlayerSeason(player_id=1,
                        team='kadachat',
                        position='C',
                        season=2025,
                        points=256,
                        games=32,
                        two_percent=.128,
                        three_percent=.256 ,
                        atr=.2))
    player_season = get_player_season_by_id(3)
    assert player_season.team == 'kadachat'

def test_delete_player(setup_database):
    assert delete_player_season(3)

def test_delete_player_season_by_player_id(setup_database):
    assert delete_player_season_by_player_id(5)
