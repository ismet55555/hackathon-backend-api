"""Data Models for FastAPI."""

from typing import List

from pydantic import BaseModel, Field

import json

class InstagramInput():
    def __init__(self, jsonDef):
        s = json.loads(jsonDef)
        self.id = None if 'id' not in s else s['id']
        self.mood = None if 'mood' not in s else s['mood']
        self.description = None if 'description' not in s else s['description']
        self.tone = None if 'tone' not in s else s['tone']


class WifiCredentials(BaseModel):
    """Wifi Credentials Model."""

    ssid: str = Field(..., example="SSID")
    password: str = Field(..., example="password")


class SystemProcessNames(BaseModel):
    """System process name list definition."""

    process_names: List[str]
