from typing import List, Optional

from pydantic import BaseModel


class Character(BaseModel):
    id: int
    name: Optional[str]
    status: Optional[str]
    species: Optional[str]
    type: Optional[str]
    gender: Optional[str]

    class Config:
        orm_mode = True


class CharacterCreate(BaseModel):
    name: str
    status: str
    species: str
    type: str
    gender: str

    def to_dict(self):
        return {
            "name": self.name,
            "status": self.status,
            "species": self.species,
            "type": self.type,
            "gender": self.gender,
        }


class CharacterCreateJson(CharacterCreate):
    id: int

    def to_dict(self):
        return {"id": self.id, **CharacterCreate.to_dict(self)}


class CharacterUpdate(BaseModel):
    name: Optional[str]
    status: Optional[str]
    species: Optional[str]
    type: Optional[str]
    gender: Optional[str]


class Characters(BaseModel):
    characters: List[Character]
