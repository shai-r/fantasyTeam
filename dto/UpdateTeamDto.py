from dataclasses import dataclass
from typing import List

@dataclass
class UpdateTeamDto:
    players: List[int]