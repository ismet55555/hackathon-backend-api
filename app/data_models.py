"""Data Models for FastAPI."""

import json
from typing import List

from openai import OpenAI
from pydantic import BaseModel, Field


class ai_bot:

    # ================= ATTRIBUTES ===============

    api_key = None
    mood = None
    tone = None
    description = None
    textPrompt = None
    imagePrompt = (None,)

    # ================= CONSTRUCTORS ===============

    def __init__(self, api_key, mood, tone, description):
        self.api_key = api_key
        self.mood = mood
        self.tone = tone
        self.description = description
        self.textPrompt = f"""Create an Instagram post given the following information. Use the description as a general guideline about the topic. The post should have the goal of becoming as viral as possible. Aim to avoid extreme views and or activism.
    Mood: {mood} Tone: {tone} Description: {description}"""
        self.imagePrompt = f"""Create an image for an Instagram post given the following information. Use the description as a general guideline about the topic. The post should have the goal of becoming as viral as possible. Aim to avoid extreme views and or activism.
    Mood: {mood} Tone: {tone} Description: {description}"""

    # ================= METHODS ===============

    # generate post content
    def generate_post_content(self):
        client = self.get_connected_client()
        result = client.chat.completions.create(
            model="gpt-3.5-turbo", messages=[{"role": "user", "content": self.textPrompt}]
        )
        return result.choices[0].message.content

    # generate post image
    def generate_post_image(self):
        client = self.get_connected_client()
        response = client.images.generate(
            model="dall-e-2",
            prompt="a white siamese cat",
            size="256x256",
            quality="standard",
            n=1,
        )
        return response.data[0].url

    # ================= HELPER METHODS ===============

    def get_connected_client(self):
        return OpenAI(api_key=self.api_key)


class WifiCredentials(BaseModel):
    """Wifi Credentials Model."""

    ssid: str = Field(..., example="SSID")
    password: str = Field(..., example="password")


class SystemProcessNames(BaseModel):
    """System process name list definition."""

    process_names: List[str]
