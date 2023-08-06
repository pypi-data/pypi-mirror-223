from typing import Any, Optional

import json
import re
import sqlite3
import time


def create_database():
    con = sqlite3.connect("sqlite3.db")
    cur = con.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS targets(
        service NOT NULL,
        ip NOT NULL,
        target_json NOT NULL,
        used_by
        );"""
    )
    cur.execute(
        """CREATE TABLE IF NOT EXISTS runs(
        exploit NOT NULL,
        start_time NOT NULL,
        duration NOT NULL,
        target_ip NOT NULL,
        flags_json,
        n_flags NOT NULL,
        used_targets,
        FOREIGN KEY(used_targets) REFERENCES targets(rowid)
        )"""
    )
    cur.execute(
        """CREATE TABLE IF NOT EXISTS flags(
        flag PRIMARY KEY,
        status NOT NULL,
        run NOT NULL,
        FOREIGN KEY(run) REFERENCES runs(rowid)
        )
        """
    )


def add_targets(targets: dict[Any, Any]) -> int:
    con = sqlite3.connect("sqlite3.db")
    cur = con.cursor()
    for service in targets:
        for ip in targets[service]:
            cur.execute(
                "INSERT INTO targets (service, ip, target_json) values (?, ?, ?)",
                (service, ip, json.dumps(targets[service][ip])),
            )
    con.commit()
    auto_id = cur.lastrowid
    if auto_id is None:
        raise Exception("database error")
    return int(auto_id)


def get_targets(
    target_ip: str | None = None,
) -> list[Any]:  # TODO: The returned value needs fixing
    con = sqlite3.connect("sqlite3.db")
    cur = con.cursor()
    if target_ip:
        cur.execute(
            "SELECT targets.rowid, service, ip, target_json FROM targets JOIN runs ON targets.rowid == runs.used_targets WHERE ip == ?",
            (target_ip,),
        )
    else:
        cur.execute(
            "SELECT targets.rowid, service, ip, target_json FROM targets JOIN runs ON targets.rowid == runs.used_targets"
        )
    all = cur.fetchall()
    return all


def saveFlag(flag: str) -> None:
    con = sqlite3.connect("sqlite3.db")
    cur = con.cursor()
    cur.execute("INSERT INTO flags values (?, ?, ?)", (flag, "UNSENT", -1))
    con.commit()


def saveExploitRun(
    exploit_name: str,
    start_time: float,
    elapsed_time: float,
    target_ip: str,
    flags: list[str],
    used_targets_id: int,
) -> None:
    con = sqlite3.connect("sqlite3.db")
    cur = con.cursor()
    cur.execute(
        "INSERT INTO runs (exploit, start_time, duration, target_ip, flags_json, n_flags) values (?, ?, ?, ?, ?, ?)",
        (
            exploit_name,
            start_time,
            elapsed_time,
            target_ip,
            json.dumps(flags),
            len(flags),
        ),
    )
    # con.commit()
    runid = cur.lastrowid
    cur.execute(
        "UPDATE targets SET used_by = ? WHERE rowid = ? ",
        (runid, used_targets_id),
    )

    for flag in flags:
        try:
            cur.execute(
                "INSERT INTO flags values (?, ?, ?)",
                (flag, "UNSENT", runid),
            )
        except sqlite3.IntegrityError:
            pass  # we should probably log somewhere that we had a duplicate
    con.commit()


def fetch_unsent_flags() -> list[str]:
    con = sqlite3.connect("sqlite3.db")
    cur = con.cursor()
    cur.execute("SELECT flag FROM flags WHERE status == 'UNSENT'")
    return [x[0] for x in cur.fetchall()]


def get_stats():
    con = sqlite3.connect("sqlite3.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM runs")
    return cur.fetchall()


create_database()
