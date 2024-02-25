"""Data Models for FastAPI."""

from typing import List

from pydantic import BaseModel, Field

import json




class WifiCredentials(BaseModel):
    """Wifi Credentials Model."""

    ssid: str = Field(..., example="SSID")
    password: str = Field(..., example="password")


class SystemProcessNames(BaseModel):
    """System process name list definition."""

    process_names: List[str]
