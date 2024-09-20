from dataclasses import dataclass
from typing import List
from dto.PlayerDto import PlayerDto


@dataclass
class TeamDto:
    team_name: str
    players: List[PlayerDto]
    team_id: int = None