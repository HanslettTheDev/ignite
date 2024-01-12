"""The main backend for ignite"""
# ignite\ignite.py
from pathlib import Path
from typing import Any, Dict, NamedTuple, List

from ignite import (CODE_EDITOR, DB_READ_ERROR, PROMPT_MESSAGES_DATA_TYPE,  CODE_EDITOR
)
from ignite.database import DatabaseHandler

#ignite_settings = {
#    "project_name": {
#       "code_editor": "nvim",
#        "language": "python",
#        "folder_location": "E:\Sotware Development\Ignite",
#        "no_of_cmd_windows": 2,
#        "activate_virtualenv": (True, "path_to_env"),
#        "monitor": (True, "monitor value"),
#        "split_view": True,
#        "virtual_desktop": (True, { bbuu
#            "virtual_desktop_name": None,
#        })
#    }
#}

class CurrentIgniteSettings(NamedTuple):
    ignite_settings: Dict[str, Any]
    error: int

class Igniter:
    def __init__(self, db_path: Path) -> None:
        self._db_handler = DatabaseHandler(db_path)

    def add(self, new_project: list[str]) -> CurrentIgniteSettings:
        """ Add a new project to the ignite database """
        ignite_settings = {
            f"{new_project[0]}": {
                "code_editor": CODE_EDITOR[int(new_project[1])],
                "folder_location": Path(new_project[2]).as_uri(),
            }
        } 
       
        previous_database_data = self._db_handler.read_ignite_settings()
        if previous_database_data.error == DB_READ_ERROR:
            return CurrentIgniteSettings(ignite_settings, previous_database_data.error)

        previous_database_data.ignite_settings.append(ignite_settings)
        write_new_data = self._db_handler.write_ignite_settings(
            previous_database_data.ignite_settings
        )

        return CurrentIgniteSettings(ignite_settings, write_new_data.error)
    
    def list_settings(self, prompt: Any = None) -> List[Dict[str, Any]] | Dict[str, Any]:
        """Return all the ignite settings that exists"""

        data = self._db_handler.read_ignite_settings()
        if prompt:
            for d in data.ignite_settings:
                if prompt in d.keys():
                    return d
        return data.ignite_settings

    @staticmethod
    def check_data(prompt: Any, index: int) -> bool:
        try:
            prompt = int(prompt) if index == 1 else prompt
        except ValueError:
            pass
        return isinstance(prompt, PROMPT_MESSAGES_DATA_TYPE[index])





