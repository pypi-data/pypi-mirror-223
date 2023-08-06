from datetime import datetime
from pathlib import Path
from typing import Union

BASE_DATA_FOLDER_NAME = "jonbot_data"

DATABASE_BACKUP = "database_backup"

LOG_FILE_FOLDER_NAME = "logs"


def os_independent_home_dir():
    return str(Path.home())


def get_base_data_folder_path(parent_folder: Union[str, Path] = os_independent_home_dir()):
    base_folder_path = Path(parent_folder) / BASE_DATA_FOLDER_NAME

    if not base_folder_path.exists():
        base_folder_path.mkdir(exist_ok=True, parents=True)

    return str(base_folder_path)


def get_log_file_path():
    log_folder_path = Path(get_base_data_folder_path()) / LOG_FILE_FOLDER_NAME
    log_folder_path.mkdir(exist_ok=True, parents=True)
    log_file_path = log_folder_path / create_log_file_name()
    return str(log_file_path)


def create_log_file_name():
    return "log_" + get_current_date_time_string() + ".log"


def get_current_date_time_string():
    return datetime.now().isoformat().replace(":", "_").replace(".", "_")


def clean_path_string(filename: str):
    return filename.replace(":", "_").replace(".", "_").replace(" ", "_")


def get_default_database_json_save_path(filename: str,
                                        timestamp: bool = False):
    if filename.endswith(".json"):
        filename.replace(".json", "")
    filename = clean_path_string(filename)
    if timestamp:
        filename += f"_{get_current_date_time_string()}"

    filename += ".json"

    save_path = Path(get_base_data_folder_path()) / DATABASE_BACKUP / f"{filename}"
    save_path.parent.mkdir(exist_ok=True, parents=True)
    return str(save_path)


def get_chroma_vector_store_path() -> str:
    return str(Path(get_base_data_folder_path()) / "chroma_vectors")
