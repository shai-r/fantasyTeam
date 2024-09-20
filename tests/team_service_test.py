from repository.database import drop_team_players_table, drop_teams_table, create_teams_table, create_team_players_table
from service.team_service import create_team, convert_from_team_id_to_team_dto
from models.TeamPlayers import TeamPlayers

def test_create_team():
    new_id = create_team(
        team_name='FFF',
        players=[TeamPlayers(player_id=1, position='C'),
                 TeamPlayers(player_id=2, position='PG'),
                 TeamPlayers(player_id=3, position='SG'),
                 TeamPlayers(player_id=4, position='SF'),
                 TeamPlayers(player_id=5, position='PF'),
                 ]
    )
    assert new_id
    new_id = create_team(
        team_name='FFU',
        players=[TeamPlayers(player_id=1, position='C'),
                 TeamPlayers(player_id=2, position='PG'),
                 TeamPlayers(player_id=3, position='SG'),
                 TeamPlayers(player_id=4, position='SF'),
                 ]
    )
    assert new_id is None
    new_id = create_team(
        team_name='FFF',
        players=[TeamPlayers(player_id=1, position='C'),
                 TeamPlayers(player_id=2, position='C'),
                 TeamPlayers(player_id=3, position='C'),
                 TeamPlayers(player_id=4, position='C'),
                 TeamPlayers(player_id=5, position='C'),
                 ]
    )
    assert new_id is None



def test_convert_from_team_and_players_to_team_dto():
    team = convert_from_team_id_to_team_dto(1)
    assert team