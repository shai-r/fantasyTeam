from dataclasses import dataclass

@dataclass
class Team:
    season: int
    C_id: int
    SG_id: int
    SF_id: int
    PF_id: int
    PG_id: int
    id: int = None