from service.player_service import convert_players_to_player_dto_for_player_endpoint


def test_convert_player_to_player_dto():
    players = convert_players_to_player_dto_for_player_endpoint('C', 0)
    assert players