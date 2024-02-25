"""Manage database."""

from pprint import pformat, pprint
from typing import List, Tuple, Union

from app.core.utility.logger_setup import get_logger
from app.core.utility.utils import overwrite_json_file, read_json_file

log = get_logger()


class Database:
    """Manage database.

    NOTE:
        Database is a local JSON file
    """

    def __init__(self, filepath: str = "database.json") -> None:
        """TODO."""
        self.db_filepath = filepath

        self.db = read_json_file(self.db_filepath)
        log.debug(f"Database file loaded: {pformat(self.db)}")
        if self.db is None:
            log.fatal(f"Failed to read database file: {self.db_filepath}")

    def remove_all_businesses(self) -> bool:
        """TODO."""
        log.info("Removing all businesses ...")
        overwrite_json_file(self.db_filepath, {})
        return True

    def get_all_business_info(self) -> dict:
        """TODO."""
        log.info("Getting all business info ...")
        self.db = read_json_file(self.db_filepath)
        return self.db

    def create_business(
        self, name: str, description: str, specifics: str, email: str, password: str
    ) -> bool:
        """TODO."""
        log.info(f"Creating business: {name}")
        self.db = read_json_file(self.db_filepath)

        # Increment next business ID number available
        next_id = len(self.db) + 1
        business_info = {
            "name": name,
            "description": description,
            "specifics": specifics,
            "email": email,
            "password": password,
        }
        self.db[str(next_id)] = business_info
        overwrite_json_file(self.db_filepath, self.db)
        return True, business_info

    def get_all_business_ids(self) -> List[int]:
        """TODO."""
        log.info(f"Getting all business IDs ...")
        self.db = read_json_file(self.db_filepath)
        return [int(id) for id in self.db.keys()]

    def get_business_info(self, business_id: int = None, name: str = None) -> Union[dict, None]:
        """TODO."""
        log.info(f"Getting business info: {business_id} ...")
        self.db = read_json_file(self.db_filepath)
        if business_id:
            return self.db.get(str(business_id), {})
        if name:
            for _, business_info in self.db.items():
                if business_info.get("name") == name:
                    return business_info
        log.error("Failed to get business info. No ID or name provided.")
        return None

    def set_business_info(self, business_id: str, key: str, value: str) -> bool:
        """TODO."""
        log.info(f"Setting business info: {business_id} ...")
        self.db = read_json_file(self.db_filepath)
        business_info = self.db.get(business_id, {})
        business_info[key] = value
        self.db[business_id] = business_info
        overwrite_json_file(self.db_filepath, self.db)
        return True

    def set_post_request_info(self, business_id: str, post_request_info: dict) -> dict:
        """TODO."""
        log.info(f"Setting post request info: {business_id} ...")
        self.db = read_json_file(self.db_filepath)
        business_info = self.db.get(business_id, {})
        business_info["post_request"] = post_request_info
        self.db[business_id] = business_info
        overwrite_json_file(self.db_filepath, self.db)
        return business_info

    def set_ai_response(self, business_id: str, ai_response: List[str]) -> dict:
        """TODO."""
        log.info(f"Setting AI responses: {business_id} ...")
        self.db = read_json_file(self.db_filepath)
        business_info = self.db.get(business_id, {})
        business_info["post_request"]["ai_response"] = ai_response
        business_info["post_request"]["in_progress"] = False
        self.db[business_id] = business_info
        overwrite_json_file(self.db_filepath, self.db)
        return business_info
