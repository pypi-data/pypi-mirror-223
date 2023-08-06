from typing import Any

from abc import abstractclassmethod
from datetime import datetime
from threading import Thread

from pwnic import db
from pwnic.config import config
from pwnic.exploits import exploits


class BaseAttacker:
    def __init__(cls) -> None:
        cls.started = False
        return

    @classmethod
    def launch_attack(cls, exploit: str, target_ip: str) -> None:
        target = db.get_targets(target_ip)
        target_id = 0
        t = Thread(
            target=exploits[exploit].run,
            args=(target_ip, target, target_id),
        )
        t.start()

    @classmethod
    def launch_all_attacks(cls) -> None:
        target = db.get_targets()
        target_ips: list[str] = [
            config["base_ip"].format(id=i)
            for i in range(1, config["highest_team_id"])
            if i != config["team_id"]
        ]

        for exploit in exploits.values():
            for ip in target_ips:
                exploit.run(ip, target)

        return

    @classmethod
    def update_targets(cls) -> None:
        new_targets = cls.fetch_targets()  # type: ignore
        db.add_targets(new_targets)

    @classmethod
    def has_game_started(cls) -> bool:
        if cls.started:
            return True

        start: datetime = config["starting_timestamp"]
        if datetime.now() > start:
            cls.started = True
            return True

        return False

    @abstractclassmethod
    def fetch_targets(cls) -> Any:
        pass
