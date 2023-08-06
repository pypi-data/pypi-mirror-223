from typing import Annotated

import os
import shutil
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, Response, UploadFile
from fastapi.responses import JSONResponse

import pwnic.db as db
from configs.Attacker import Attacker
from pwnic.exploits import exploits, load_exploit
from pwnic.submitter import Submitter
from pwnic.utils import install_package as package_install

app = FastAPI()


@app.post("/upload")
def upload_exploit(
    type: Annotated[str, Form()],
    name: Annotated[str, Form()],
    files: Annotated[list[UploadFile], File()],
) -> JSONResponse:
    path = f"exploits/{type}/{name}"

    os.makedirs(f"/tmp/{path}", exist_ok=True)
    for f in files:
        with open(f"/tmp/{path}/{f.filename}", "wb") as fs:
            fs.write(f.file.read())

    try:
        load_exploit(type, name, dir=f"/tmp/{path}")
    except ValueError:
        return JSONResponse(f"{type} is not valid", 422)
    except Exception:
        return JSONResponse("Unhandled Exception while loading exploit", 500)

    shutil.copytree(src=f"/tmp/{path}", dst=path, dirs_exist_ok=True)
    load_exploit(type, name)

    return JSONResponse({f.filename: f.size for f in files}, 201)


@app.get("/stats")
def get_stats():
    return db.get_stats()


@app.get("/install")
def install_package(package: str) -> dict[str, str]:
    if package_install(package):
        return {package: "installed"}
    else:
        return {package: "error"}


@app.get("/run")
def run_exploit(
    exploit: str, target: str, fetch_new_targets: bool = False
) -> Response:
    if exploit not in exploits:
        raise HTTPException(
            status_code=400,
            detail=f"{exploit} is not a valid exploit. It must be one of {exploits.keys()}",
        )
    if fetch_new_targets:
        Attacker.update_targets()

    Attacker.launch_attack(exploit, target)
    return JSONResponse("ok", 200)


@app.get("/launch_attacks")
def launch_exploits() -> None:
    Attacker.launch_all_attacks()


@app.get("/submit")
def submit_flags():
    flags = Submitter.fetch_unsent()
    out = Submitter.submit_flags(flags)
    print(out)

    if out is None:
        return JSONResponse("There was an error with the submit", 500)
    return out


@app.get("/addFlag")
def add_flag(flag: str) -> None:
    db.saveFlag(flag)


@app.get("/resetDB")
def reset_DB():
    os.remove("sqlite3.db")
    db.create_database()

    return {"ok": "database cleared"}
