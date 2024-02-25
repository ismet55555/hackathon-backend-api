"""Class handling twitter stuff."""

from typing import Tuple

import os
import base64

from requests_oauthlib import OAuth1
import requests
from fastapi import HTTPException

from app.core.utility.logger_setup import get_logger

log = get_logger()

class Twitter:
    """Class handling twitter stuff."""

    def __init__(self) -> None:
        """Run Constructor."""
        pass
        # self.bearer_token = self._get_twitter_bearer_token()
        # if not self.bearer_token:
        #     log.fatal("Failed to obtain Twitter bearer token from environment")
        #     raise SystemExit

    # def _get_twitter_bearer_token(self) -> str:
    #     """Fetch Twitter bearer token."""
    #     log.info("Getting Twitter bearer token ...")
    #     key = os.getenv("TWITTER_API_KEY")
    #     secret = os.getenv("TWITTER_API_KEY_SECRET")
    #     bearer_token_credentials = base64.b64encode(f"{key}:{secret}".encode("utf-8")).decode("utf-8")
    #     headers = {
    #         "Authorization": f"Basic {bearer_token_credentials}",
    #         "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
    #     }
    #     response = requests.post(
    #         "https://api.twitter.com/oauth2/token",
    #         headers=headers,
    #         data={"grant_type": "client_credentials"},
    #     )
    #     if response.status_code != 200:
    #         raise HTTPException(status_code=500, detail="Failed to obtain bearer token")
    #
    #     return response.json()["access_token"]


    def post_tweet(self, tweet_text: str, tweet_image_url: str) -> Tuple[bool, str]:
        """Post a tweet."""
        log.info("Posting tweet ...")
        response = requests.get(tweet_image_url, timeout=10)
        if response.status_code != 200:
            log.error(f"Failed to download image: {response.text}")
            raise HTTPException(status_code=400, detail="Could not download this image")

        #   Convert the image to the format required by the APIv1
        files = {"media": response.content}
        media_upload_url = "https://upload.twitter.com/1.1/media/upload.json"

        oauth = OAuth1(
            os.getenv("TWITTER_API_KEY"),
            os.getenv("TWITTER_API_KEY_SECRET"),
            os.getenv("TWITTER_ACCESS_TOKEN"),
            os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
        )

        response = requests.post(media_upload_url, files=files, auth=oauth, timeout=10)

        # Before attempting to decode the response, check if it was successful
        if response.status_code != 200:
            # Log or print the error response for debugging
            error_message = f"Failed to upload media: Status code: {response.status_code}, Response: {response.text}"
            log.error(error_message)
            raise HTTPException(status_code=500, detail=error_message)

        # Attempt to decode the JSON response
        try:
            media_id = response.json()["media_id_string"]
            if not media_id:
                raise HTTPException(status_code=500, detail="Media ID not found in the response")
        except ValueError as error:
            raise HTTPException(status_code=500, detail=f"JSON decode error: {error}") from error

        #   Step 3: Post the tweet with the image using Twitter API v2
        tweet_url = "https://api.twitter.com/2/tweets"
        headers = {
            "Authorization": f"Bearer {self._get_twitter_bearer_token()}",
            "Content-Type": "application/json",
        }
        payload = {
            "text": tweet_text,
            "media": {
                "media_ids": [
                    media_id
                ]  # Replace media_id with the actual media ID from the upload response #????????????
            },
        }
        response = requests.post(tweet_url, json=payload, headers=headers)

        if response.status_code != 201:
            raise HTTPException(
                status_code=response.status_code, detail=f"Failed to post tweet: {response.text}"
            )

        return True, response.json()["data"]["id"]
