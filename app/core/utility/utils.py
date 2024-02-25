"""General utility Functions."""

import json
import os
import subprocess
from json import JSONDecodeError
from pathlib import Path
from stat import filemode
from subprocess import CalledProcessError
from typing import Any, List, Union

from app.core.utility.logger_setup import get_logger

log = get_logger()


def run_shell_script_file(sh_file_path: str) -> None:
    """Run a shell script file.

    Args:
        sh_file_path: Local absolute file path of shell script file
    """
    log.info(f"Running shell script file: {sh_file_path} ...")
    if not Path(sh_file_path).is_file():
        raise FileNotFoundError(f"Local shell script file does not exist: {sh_file_path}")

    if not Path(sh_file_path).stat().st_mode & 0o100:
        file_permissions = filemode(Path(sh_file_path).stat().st_mode)
        raise PermissionError(
            f"Shell script file is not executable: {sh_file_path}. "
            f"File permissions: {file_permissions}"
        )

    try:
        subprocess.run([sh_file_path], check=True)
    except CalledProcessError as error:
        log.error(f"Failed running shell script file: {error}")
        raise
    log.debug("Successfully ran shell script file")


def update_top_level_key_in_json_file(json_file_path: str, key: str, value: Any) -> bool:
    """Update a JSON file with a key/value pair.

    Args:
        json_file_path: Local absolute file path of JSON file
        key: Top level key to update
        value: Value to update the key with

    Returns:
        True if successful, False otherwise
    """
    log.debug(f"Updating JSON file: {json_file_path} ...")
    if not Path(json_file_path).is_file():
        log.error(f"Local JSON file does not exist: {json_file_path}")
        return False

    try:
        with open(json_file_path, "r", encoding="utf-8") as json_file:
            json_data = json.load(json_file)
    except (JSONDecodeError, IOError, OSError) as error:
        log.error(f"Failed loading local JSON file: {error}")
        return False

    json_data[key] = value

    try:
        with open(json_file_path, "w", encoding="utf-8") as json_file:
            json.dump(json_data, json_file, indent=4)
    except (JSONDecodeError, IOError, OSError) as error:
        log.error(f"Failed encoding JSON file: {error}")
        return False

    log.debug(f"Successfully updated JSON file: {json_file_path}")
    return True


def create_file(local_filepath: str, file_content: str = "") -> bool:
    """Create a local file with optional content.

    Args:
        local_filepath: Local absolute file path to create
        file_content: Optional content to write to file

    Returns:
        True if successful, False otherwise
    """
    log.debug(f"Creating local file: {local_filepath} ...")
    try:
        with open(local_filepath, "w", encoding="utf-8") as local_file:
            local_file.write(file_content)
    except (IOError, OSError) as error:
        log.error(f"Failed to create local file: {error}")
        return False
    log.debug(f"Successfully created local file: {local_filepath}")
    return True


def delete_file(local_filepath: str) -> bool:
    """Delete a local file.

    Args:
        local_filepath: Local absolute file path to delete

    Returns:
        True if successful, False otherwise
    """
    log.debug(f"Deleting local file: {local_filepath} ...")
    try:
        os.remove(local_filepath)
    except OSError as error:
        log.error(f"Failed to delete local file: {error}")
        return False
    log.debug(f"Successfully deleted local file {local_filepath}")
    return True


def is_file_present(local_filepath: str) -> bool:
    """Check if a file on local file system exists.

    Args:
        local_filepath: Local absolute file path to check

    Returns:
        True if file exists, else False
    """
    log.debug(f"Checking if local file exists: {local_filepath} ...")
    if not Path(local_filepath).is_file():
        log.error(f"Failed to find local file does not exist: {local_filepath}")
        return False
    log.debug(f"Successfully found local file exists: {local_filepath}")
    return True


def read_file(local_filepath: str, lines_to_read: int = -1) -> Union[List[str], None]:
    """Read a process state file and return the first line of the content.

    Args:
        local_filepath: Local absolute file path to read
        lines_to_read: Number of lines to read from file (-1 for all)

    Returns:
        List of lines read from file

    """
    log.debug(f"Reading local file: {local_filepath} ...")
    if not Path(local_filepath).is_file():
        log.error(f"Failed to read local file does not exist: {local_filepath}")
        return []

    try:
        with open(local_filepath, "r", encoding="utf-8") as local_file:
            if lines_to_read == -1:
                file_content = local_file.readlines()
            else:
                file_content = local_file.readlines()[:lines_to_read]
    except (IOError, OSError, FileNotFoundError) as error:
        log.error(f"Failed to read local file: {error}")
        return None

    log.debug(f"Successfully read local file: {local_filepath}")
    return file_content

def read_json_file(local_filepath: str) -> Union[dict, None, Any]:
    """Read a JSON file and return the content.

    Args:
        local_filepath: Local absolute file path to read

    Returns:
        Dictionary of JSON file content
    """
    log.debug(f"Reading local JSON file: {local_filepath} ...")
    if not Path(local_filepath).is_file():
        log.error(f"Failed to read local JSON file does not exist: {local_filepath}")
        return None

    try:
        with open(local_filepath, "r", encoding="utf-8") as json_file:
            json_data = json.load(json_file)
    except (JSONDecodeError, IOError, OSError) as error:
        log.error(f"Failed to read local JSON file: {error}")
        return None

    log.debug(f"Successfully read local JSON file: {local_filepath}")
    return json_data


def overwrite_file(local_filepath: str, file_content: str) -> bool:
    """Overwrite a local file with content.

    Args:
        local_filepath: Local absolute file path to overwrite
        file_content: Content to write to file

    Returns:
        True if successful, False otherwise
    """
    log.debug(f"Overwriting local file: {local_filepath} ...")
    try:
        with open(local_filepath, "w", encoding="utf-8") as local_file:
            local_file.write(file_content)
    except (IOError, OSError, FileNotFoundError) as error:
        log.error(f"Failed to overwrite local file: {error}")
        return False
    log.debug(f"Successfully overwritten local file: {local_filepath}")
    return True

def overwrite_json_file(local_filepath: str, json_data: dict) -> bool:
    """Overwrite a local JSON file with content.

    Args:
        local_filepath: Local absolute file path to overwrite
        json_data: JSON data to write to file

    Returns:
        True if successful, False otherwise
    """
    log.debug(f"Overwriting local JSON file: {local_filepath} ...")
    try:
        with open(local_filepath, "w", encoding="utf-8") as json_file:
            json.dump(json_data, json_file, indent=4)
    except (JSONDecodeError, IOError, OSError, FileNotFoundError) as error:
        log.error(f"Failed to overwrite local JSON file: {error}")
        return False
    log.debug(f"Successfully overwritten local JSON file: {local_filepath}")
    return True

def is_process_running(process_name: str) -> bool:
    """Check if a process is running.

    Args:
        process_name: Name of the process to check

    Returns:
        True if process is running, else False
    """
    log.debug(f"Checking if process is running: {process_name} ...")
    try:
        subprocess.run(["pgrep", process_name], check=True, shell=True)
    except CalledProcessError:
        log.debug(f"Process is not running: {process_name}")
        return False
    log.debug(f"Process is running: {process_name}")
    return True
