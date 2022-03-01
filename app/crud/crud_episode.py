from fastapi.encoders import jsonable_encoder

from app.crud.base import CRUDBase, CreateSchemaType, ModelType
from app import schema
from app import models
from sqlalchemy.orm import Session
from app import errors


class CRUDEpisode(
    CRUDBase[models.Episode, schema.postEpisodeQuery, schema.EpisodeUpdate]
):
    def get_by_episode_season(
        self, db: Session, episode_number: int, episode_season: int
    ):
        return (
            db.query(self.model)
            .filter(
                self.model.episode == episode_number,
                self.model.season == episode_season,
            )
            .first()
        )

    def create(self, db: Session, obj_in: schema.postEpisodeQuery) -> models.Episode:
        episode_db = self.get_by_episode_season(
            db=db, episode_number=obj_in.episode, episode_season=obj_in.season
        )

        if episode_db:
            raise errors.ElementAlreadyExistsError(
                f"episode {obj_in.episode} season {obj_in.season} already in the database"
            )

        obj_in_data = jsonable_encoder(obj_in)
        if "characters" in obj_in_data:
            del obj_in_data["characters"]

        db_obj = self.model(**obj_in_data)  # type: ignore

        if obj_in.characters:
            characters = (
                db.query(models.Character)
                .filter(models.Character.id.in_(obj_in.characters))
                .all()
            )
            missing_characters = set(obj_in.characters) - set(
                [c.id for c in characters]
            )

            if missing_characters:
                raise errors.CharactersAlreadyExistError(
                    f"characters {missing_characters} not in the database"
                )

            db_obj.characters = characters

        db.add(db_obj)
        db.commit()
        return db_obj


episode = CRUDEpisode(models.Episode)
