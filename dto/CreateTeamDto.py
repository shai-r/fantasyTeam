from dataclasses import dataclass
from typing import List
from models.TeamPlayers import TeamPlayers


@dataclass
class CreateTeamDto:
    team_name: str
    players: List[TeamPlayers]
    team_id: int = None