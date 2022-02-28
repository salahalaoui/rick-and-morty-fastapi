import json
import logging
import sys
import typing

import requests
from app import schema

logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

ListingPageGenerator = typing.Generator[typing.Tuple[bytes, int], None, None]
ListingDataGenerator = typing.Generator[
    typing.Tuple[int, typing.Dict[str, str]], None, None
]


def page_fetcher(fullpath) -> ListingPageGenerator:
    with open(fullpath) as file:
        data = json.load(file)
        for idx, val in enumerate(data):
            logger.info("Fetching element %d", idx)
            yield idx, val


def parser(schemaElement, fetcher: ListingPageGenerator) -> ListingDataGenerator:
    for idx, val in fetcher:
        logger.info("Parsing element %d", idx)
        val["season"] = val["episode"]
        yield schemaElement(**val)


def episode_injector(parser: ListingDataGenerator):
    for episode in parser:

        r = requests.post(
            "http://app:8000/episodes",
            json=episode.to_dict(),
            headers={"accept": "application/json", "Content-Type": "application/json"},
        )
        logger.info(f"Adding episode {episode.id}... status code {r.status_code}")


def character_injector(parser: ListingDataGenerator):
    for character in parser:
        r = requests.post(
            "http://app:8000/characters",
            json=character.to_dict(),
            headers={"accept": "application/json", "Content-Type": "application/json"},
        )
        logger.info(f"Adding character {character.id}... status code {r.status_code}")


character_injector(
    parser(
        schema.CharacterCreateJson, page_fetcher("documents/rick_morty-characters_v1.json")
    ),
)

episode_injector(
    parser(schema.EpisodeCreateJson, page_fetcher("documents/rick_morty-episodes_v1.json")),
)
