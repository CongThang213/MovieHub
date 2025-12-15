from dataclasses import dataclass


@dataclass
class FilmCast:
    """
    Represents the relationship between a film and a cast member with their role.
    """

    cast_id: str
    role: str = "Actor"
    character_name: str = ""
