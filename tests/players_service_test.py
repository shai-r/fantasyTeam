from service.player_service import convert_player_to_player_dto


def test_convert_player_to_player_dto():
    players = convert_player_to_player_dto('C', 0)
    assert players