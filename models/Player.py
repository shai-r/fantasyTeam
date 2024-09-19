from dataclasses import dataclass

@dataclass
class Player:
    api_id: int
    player_name: str
    id: int = None
