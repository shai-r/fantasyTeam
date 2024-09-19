from dataclasses import dataclass

@dataclass
class Player:
    api_id: str
    player_name: str
    id: int = None
