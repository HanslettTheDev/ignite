"""This module provides a simple database interface for ignite to interact with"""
# ignite\database.py

import configparser
import json

from pathlib import Path
from typing import Any, Dict, List, NamedTuple
from ignite import DB_READ_ERROR, DB_WRITE_ERROR, JSON_ERROR, SUCCESS, __app_name__

DEFAULT_DB_PATH = Path.joinpath(Path.cwd(), "." + Path.home().stem + "_ignite_db.json")


class DBResponse(NamedTuple):
    ignite_settings: list[Dict[str, Any]]
    error: int


class DatabaseHandler:
    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path

    def read_ignite_settings(self) -> DBResponse:
        try:
            with self._db_path.open("r") as db:
                try:
                    return DBResponse(json.load(db), SUCCESS)
                except json.JSONDecodeError: # Catch wrong Json formats
                    return DBResponse([], JSON_ERROR)
        except OSError: # catch file IO problems
            return DBResponse([], DB_READ_ERROR)
    
    def write_ignite_settings(self, ignite_settings: List[Dict[str, Any]]) -> DBResponse:
        try:
            with self._db_path.open("w") as db:
                json.dump(ignite_settings, db, indent=4)
            return DBResponse(ignite_settings, SUCCESS)
        except OSError:
            return DBResponse(ignite_settings, DB_WRITE_ERROR)

def get_database_path(config_file: Path) -> Path:
    """Return the current path of the ignites database"""
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)

    return Path(config_parser["General"]["database"])

def create_database(db_path: Path) -> int:
    """Create the ignite database for storing some base values"""
    try:
        db_path.write_text("[]")
        return SUCCESS
    except OSError:
        return DB_WRITE_ERROR
