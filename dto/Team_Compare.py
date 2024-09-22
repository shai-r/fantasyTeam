from dataclasses import dataclass


@dataclass
class TeamCompare:
    team: str
    points: int
    twoPercent: float
    threePercent: float
    ATR: float
    PPG: float