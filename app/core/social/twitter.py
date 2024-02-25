"""Class handling twitter stuff."""

import urllib

import tweepy

from app.core.utility.logger_setup import get_logger

log = get_logger()


class Twitter:
    """Class handling twitter stuff."""

    api_key = None
    api_secret = None
    access_token = None
    access_token_secret = None

    def __init__(
        self, api_key: str, api_secret: str, access_token: str, access_token_secret: str
    ) -> None:
        """Run Constructor."""
        self.api_key = api_key
        self.api_secret = api_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        return

    def post(self, content: str, image_url: str) -> None:
        log.info("Posting Twitter post ...")
        client_v1 = self.get_twitter_conn_v1(
            self.api_key, self.api_secret, self.access_token, self.access_token_secret
        )
        client_v2 = self.get_twitter_conn_v2(
            self.api_key, self.api_secret, self.access_token, self.access_token_secret
        )

        urllib.request.urlretrieve(image_url, "tempImage.png")

        media = client_v1.media_upload(filename="tempImage.png")
        media_id = media.media_id

        client_v2.create_tweet(text=content, media_ids=[media_id])

    def get_twitter_conn_v1(
        self, api_key: str, api_secret: str, access_token: str, access_token_secret: str
    ) -> tweepy.API:
        """Get twitter conn 1.1"""
        auth = tweepy.OAuth1UserHandler(api_key, api_secret)
        auth.set_access_token(
            access_token,
            access_token_secret,
        )
        return tweepy.API(auth)

    def get_twitter_conn_v2(
        self, api_key: str, api_secret: str, access_token: str, access_token_secret: str
    ) -> tweepy.Client:
        """Get twitter conn 2.0"""
        client = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
        )

        return client
