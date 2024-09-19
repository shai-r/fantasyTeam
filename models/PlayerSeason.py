from dataclasses import dataclass

@dataclass
class PlayerSeason:
    player_id: int
    team: str
    position: str
    season: int
    points: int
    games: int
    two_percent: float
    three_percent: float
    atr: float
    id: int = None