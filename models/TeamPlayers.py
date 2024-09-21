from dataclasses import dataclass


@dataclass
class TeamPlayers:
    player_id: int
    position: str = None
    id: int = None
    team_id: int = None