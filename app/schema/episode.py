from datetime import datetime
from typing import List, Optional, Set

from app.schema import OrmBase
from app.schema.character import Character
from pydantic import BaseModel, Field, validator


class EpisodeCreate(BaseModel):
    name: str
    air_date: datetime
    episode: int
    season: int

    class Config:
        orm_mode = True

    def to_dict(self):
        data = {
            "name": self.name,
            "air_date": str(self.air_date),
            "episode": self.episode,
            "season": self.season,
        }
        return data


class postEpisodeQuery(EpisodeCreate):
    characters: Optional[List[int]]


class Episode(EpisodeCreate):
    id: int

    def to_dict(self):
        return {"id": self.id, **EpisodeCreate.to_dict(self)}


class EpisodeDB(EpisodeCreate):
    id: int
    character_ids: Optional[List[int]]


class EpisodeWithCharacters(OrmBase, EpisodeCreate):
    id: int
    characters: Optional[List[Character]]


class Episodes(BaseModel):
    episodes: List[Episode]


class EpisodeCreateJson(Episode):
    characters: Optional[List[int]]

    @validator("air_date", pre=True)
    def air_date_validate(cls, v):
        return datetime.strptime(v, "%B %d, %Y")

    @validator("episode", pre=True)
    def episode_validate(cls, v):
        return int(v.split("E")[1])

    @validator("season", pre=True)
    def season_validate(cls, v):
        return int(v.split("E")[0].split("S")[1])

    def to_dict(self):
        return {**Episode.to_dict(self), "characters": self.characters}


class EpisodeUpdate(BaseModel):
    name: Optional[str]
    air_date: Optional[datetime]


class addCharactersQuery(BaseModel):
    episode_id: int
    character_ids: Set[int]
