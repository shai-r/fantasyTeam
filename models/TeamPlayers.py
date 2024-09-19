from dataclasses import dataclass


@dataclass
class TeamPlayers:
    team_id: int
    player_id: int
    position: str
    id: int = None