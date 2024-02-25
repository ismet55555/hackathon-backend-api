"""Server routes definitions."""

import os
from pprint import pprint
from typing import Any, Dict

import tweepy

import requests

from dotenv import load_dotenv
from fastapi import APIRouter, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.core.ai_bot.ai_bot import AiBot
from app.core.database.database import Database
from app.core.fastapi_config import Settings
from app.core.social.twitter import Twitter
from app.core.utility.logger_setup import get_logger
from app.core.utility.timing_middleware import TimingMiddleware
from app.core.utility.utils import read_json_file

import urllib.request

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
    async def generate_post_content(self):
        client = self.get_connected_client()
        result = await client.chat.completions.create(
            model="gpt-3.5-turbo", messages=[{"role": "user", "content": self.textPrompt}]
        )
        return result.choices[0].message.content

    # generate post image
    async def generate_post_image(self):
        client = self.get_connected_client()
        response = await client.images.generate(
            model="dall-e-2",
            prompt="a white siamese cat",
            size="256x256",
            quality="standard",
            n=1,
        )
        return response.data[0].url

    # ================= HELPER METHODS ===============

    def get_connected_client(self):
        return AsyncOpenAI(api_key=self.api_key)



log = get_logger()
load_dotenv()

# Retrieving API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    ERROR_MESSAGE = "No OpenAI key found;. Make sure your .env file is set up correctly"
    log.fatal(ERROR_MESSAGE)
    raise ValueError(ERROR_MESSAGE)


######################################################################
#              FastAPI init
######################################################################
def get_app():
    """Get application handle and add any middleware.

    Returns:
        Application object
    """
    settings = Settings()

    # Create FastAPI application
    _app = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.PROJECT_DESCRIPTION,
        version=settings.PROJECT_VERSION,
    )
    # Add CORS Middleware
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add Timing Middleware to log request times
    _app.add_middleware(TimingMiddleware)

    # Define static file location
    _app.mount("/static", StaticFiles(directory="app/front-end/static"), name="static")

    # Add route rate limiter
    limiter = Limiter(key_func=get_remote_address)
    _app.state.limiter = limiter
    _app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    return _app


app = get_app()
database = Database("app/core/database/database.json")
twitter = Twitter()
templates = Jinja2Templates(directory="app/front-end/templates")


#################################################################################
#                                index.html
#################################################################################
@app.get("/", response_class=HTMLResponse)
def index_info_html_page(request: Request) -> Any:
    """Front info page."""
    return templates.TemplateResponse("index.html", {"request": request})


#################################################################################
#                                 Default
#################################################################################
@app.get("/health")
def app_health_check() -> Dict[str, str]:
    """Application health check status."""
    return {"status": "healthy"}


#################################################################################
#                           Social Posts
#################################################################################
social_api_router = APIRouter(tags=["social"])


@app.post("/post_to_twitter")
def post_to_twitter(tweet_text: str, tweet_image_url: str) -> dict:
    """Post a tweet."""
    success, tweet_id = twitter.post_tweet(tweet_text, tweet_image_url)
    return {"success": success, "tweet_id": tweet_id}


@app.post("/post_to_instagram")
def post_to_instagram(instagram_text: str, instagram_image_url: str) -> dict:
    """Post a tweet."""
    # TODO
    success, post_id = False, "34353453"
    return {"success": success, "tweet_id": post_id}


app.include_router(social_api_router, prefix="/social")


#################################################################################
#                                 BUSINESS
#################################################################################
business_api_router = APIRouter(tags=["business"])


@business_api_router.get("/create")
def create_a_business(
    name: str, description: str, specifics: str, email: str, password: str
) -> dict:
    """Create a business."""
    success = database.create_business(name, description, specifics, email, password)
    return {"success": success}


@business_api_router.get("/get_business_info_with_id")
def get_business_info_with_id(id: str) -> dict:
    """Get business info with id."""
    info = database.get_business_info(int(id))
    return {"info": info}


@business_api_router.get("/get_business_info_with_name")
def get_business_info_with_name(name: str) -> dict:
    """Get business info with name."""
    info = database.get_business_info(name=name)
    return {"info": info}


@business_api_router.get("/get_all_Business_info")
def get_all_business_info() -> dict:
    """Get all business info."""
    info = database.get_all_business_info()
    return {"ids": info}


@business_api_router.get("/get_all_business_ids")
def get_all_business_ids() -> dict:
    """Get all business ids."""
    info = database.get_all_business_ids()
    return {"ids": info}


@business_api_router.post("/remove_all_businesses")
def remove_all_businesses() -> dict:
    """Get all business ids."""
    success = database.remove_all_businesses()
    return {"success": success}


app.include_router(business_api_router, prefix="/business")


#################################################################################
#                                 AI API
#################################################################################
ai_api_router = APIRouter(tags=["ai_api"])


@ai_api_router.post("/send_post_request")
async def send_post_request(id: str, mood: str, tone: str, description: str) -> bool:
    """Send a post request to OpenAPI."""
    info = {
        "caption_mood": mood,
        "cpation_tone": tone,
        "caption_description": description,
        "picture_prompt": description,
        "picture_size": "256x256",
        "in_progress": True,
    }
    database.set_post_request_info(business_id=id, post_request_info=info)

    pprint(database.get_business_info(business_id=id))

    # userInput = json.loads(jsonInput)

    our_ai_bot = AiBot(
        api_key=OPENAI_API_KEY,
        mood=mood,
        tone=tone,
        description=description,
    )

    # send post request
    generated_content = await our_ai_bot.generate_post_content()
    generated_image = await our_ai_bot.generate_post_image()

    responses = {"caption_text": generated_content, "picture_url": generated_image}

    # add post info to database
    database.set_ai_response(business_id=id, ai_response=responses)

    # respond success
    return True


@ai_api_router.post("/check_post_status")
def check_post_status() -> bool:
    """Check status of OpenAPI request."""
    return True


@ai_api_router.get("/get_post_data")
def get_post_data(id: str) -> dict:
    """Get the data returened from OpenAPI if ready."""
    business_info = database.get_business_info(id)
    return business_info["post_request"]["ai_response"]


app.include_router(ai_api_router, prefix="/ai_api")

#################################################################################
#                                 Social Media
#################################################################################
social_api_router = APIRouter(tags=["social"])


@social_api_router.post("/post_to_instagram")
def post_to_instagram() -> bool:
    """Post to Instagram."""
    return True


@social_api_router.post("/post_to_twitter")
def post_to_twitter(id: str) -> bool:
    """Post to Twitter/x."""

    def get_twitter_conn_v1(api_key, api_secret, access_token, access_token_secret) -> tweepy.API:
        """Get twitter conn 1.1"""

        auth = tweepy.OAuth1UserHandler(api_key, api_secret)
        auth.set_access_token(
            access_token,
            access_token_secret,
        )
        return tweepy.API(auth)

    def get_twitter_conn_v2(api_key, api_secret, access_token, access_token_secret) -> tweepy.Client:
        """Get twitter conn 2.0"""

        client = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
        )

        return client

    api_key = os.getenv("TWITTER_API_KEY")
    api_secret = os.getenv("TWITTER_API_SECRET")
    access_token = os.getenv("TWITTER_ACCESS_TOKEN")
    access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

    client_v1 = get_twitter_conn_v1(api_key, api_secret, access_token, access_token_secret)
    client_v2 = get_twitter_conn_v2(api_key, api_secret, access_token, access_token_secret)

    # get image and content from database
    ai_response = database.get_business_info(business_id=id)["post_request"]["ai_response"]

    urllib.request.urlretrieve(ai_response["picture_url"], "tempImage.png")

    media = client_v1.media_upload(filename="tempImage.png")
    media_id = media.media_id

    client_v2.create_tweet(text=ai_response["caption_text"], media_ids=[media_id])

    return True


app.include_router(social_api_router, prefix="/social")
