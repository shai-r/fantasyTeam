from dataclasses import dataclass

@dataclass
class Team:
    team_id: int
    C: int
    SG: int
    SF: int
    PF: int
    PG: int