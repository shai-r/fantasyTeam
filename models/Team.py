from dataclasses import dataclass

@dataclass
class Team:
    team_name: str
    season: int
    id: int = None