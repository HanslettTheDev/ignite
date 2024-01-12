""" Top Level Package for Ignite """
# ignite/__init__.py

__app_name__ = "ignite"
__version__ = "1.0.0"

(
    SUCCESS,
    DIR_ERROR,
    FILE_ERROR,
    DB_READ_ERROR,
    DB_WRITE_ERROR,
    JSON_ERROR,
    ID_ERROR,
) = range(7)


ERRORS = {
    DIR_ERROR: "Config directory error",
    FILE_ERROR: "Config file error",
    DB_READ_ERROR: "database read error",
    DB_WRITE_ERROR: "database write error",
    ID_ERROR: "Ignite Key Error",
}

PROMPT_MESSAGES = [
    "Enter the name of your project(e.g ignite)",
    "Select a code editor [1.Neovim 2.VSCode]",
    "Enter the path to your project",
]


PROMPT_MESSAGES_DATA_TYPE = (
    str,
    int,
    str,
)


CODE_EDITOR = {
    1: "nvim",
    2: "code"
}

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

