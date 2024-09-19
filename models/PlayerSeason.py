from dataclasses import dataclass
from enums.Position_enum import Position

@dataclass
class PlayerSeason:
    player_id: int
    team: str
    position: Position
    season: int
    points: int
    games: int
    two_percent: float
    three_percent: float
    atr: float
    ppg: float
    id: int = None