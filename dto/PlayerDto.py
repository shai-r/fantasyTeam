from dataclasses import dataclass
from typing import List

@dataclass
class PlayerDto:
    player_id: int
    playerName: str
    team: str
    position: str
    season: List[int]
    points: int
    games: int
    twoPercent: float
    threePercent: float
    ATR: float
    PPG: float