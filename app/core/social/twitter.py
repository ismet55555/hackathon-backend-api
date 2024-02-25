"""Class handling twitter stuff."""

import base64
import os
from typing import Tuple

import requests
from fastapi import HTTPException
from requests_oauthlib import OAuth1

from app.core.utility.logger_setup import get_logger

import urllib
import tweepy

log = get_logger()


class Twitter:
    """Class handling twitter stuff."""

    api_key = None
    api_secret = None
    access_token = None
    access_token_secret = None

    def __init__(self, api_key, api_secret, access_token, access_token_secret) -> None:
        """Run Constructor."""
        self.api_key = api_key
        self.api_secret = api_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        return

    def post(self, content, imageUrl):
        client_v1 = self.get_twitter_conn_v1(self.api_key, self.api_secret, self.access_token, self.access_token_secret)
        client_v2 = self.get_twitter_conn_v2(self.api_key, self.api_secret, self.access_token, self.access_token_secret)

        urllib.request.urlretrieve(imageUrl, "tempImage.png")

        media = client_v1.media_upload(filename="tempImage.png")
        media_id = media.media_id

        client_v2.create_tweet(text=content, media_ids=[media_id])

    def get_twitter_conn_v1(self, api_key, api_secret, access_token, access_token_secret) -> tweepy.API:
        """Get twitter conn 1.1"""

        auth = tweepy.OAuth1UserHandler(api_key, api_secret)
        auth.set_access_token(
            access_token,
            access_token_secret,
        )
        return tweepy.API(auth)

    def get_twitter_conn_v2(self, api_key, api_secret, access_token, access_token_secret) -> tweepy.Client:
        """Get twitter conn 2.0"""

        client = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
        )

        return client

