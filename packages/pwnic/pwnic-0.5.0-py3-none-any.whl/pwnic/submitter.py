from typing import Any

import logging
from collections.abc import Iterable

import requests

from pwnic import db
from pwnic.config import config

log = logging.getLogger(__name__)


class Submitter:
    @classmethod
    def __init__(cls) -> None:
        return

    @classmethod
    def submit_flags(cls, flags: list[str]) -> Any | None:
        try:
            """
            this may be different for other CTFs
            """
            log.info(f"Submitting flags: {flags}")
            response: Any = requests.put(
                url=config.submit_url,
                headers={"X-Team-Token": config.team_token},
                json=flags,
                timeout=config["timeout"],  # nosec
            )  # .json()  # this is a list
            log.info(f"Got {response = }")
            return response.json()
        except requests.ConnectTimeout as e:
            log.exception("Gameserver didn't answer!")

        except requests.JSONDecodeError as e:
            log.critical(f"JSON decoding error!\n")
            raise e

        except Exception as e:
            log.exception(f"Unhandled exception was raised!")

        return None

    @classmethod
    def fetch_unsent(cls) -> list[str]:
        return db.fetch_unsent_flags()
