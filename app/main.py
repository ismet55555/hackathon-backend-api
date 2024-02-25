"""Server routes definitions."""

from typing import Any, Dict, List

from fastapi import APIRouter, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from app.core.fastapi_config import Settings
from app.core.logs.logs import Logs
from app.core.utility.logger_setup import get_logger
from app.core.utility.timing_middleware import TimingMiddleware

import requests
import os
from dotenv import load_dotenv

log = get_logger()

load_dotenv()
######################################################################
#|
#|              OpenAI API Key Info
#|
######################################################################

#Retrieving API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
#Ensure API key is loaded right
if not OPENAI_API_KEY:
    raise ValueError("No OpenAI key found;. Make sure your .env file is set up correctly")

#   Headers for authentication with the OpenAI API
headers = {
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
        "Content-Type": "application/json"
    }

######################################################################
#|
#|
#|
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
logs = Logs()
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
#                                 Image Generator
#################################################################################
# Assuming the rest of your initial setup remains the same

class ImagePrompt(BaseModel):
    prompt: str
    n: int = 1  # Number of images to generate
    size: str = "1024x1024"  # Pixels

@app.post("/generate-image")
async def generate_image(request: ImagePrompt):
    """
    Receives an image generation prompt from the front-end, sends it to OpenAI's API,
    and returns the generated image(s) to the front-end.
    """
    # OpenAI API Settings
    url = "https://api.openai.com/v1/images/generations"
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": request.prompt,
        "n": request.n,
        "size": request.size,
        "model": "dall-e-3",
        "quality": "hd"
    }

    # Make the API request
    response = requests.post(url, json=payload, headers=headers)
    
    # Check for errors
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=f"API request failed: {response.text}")
    
    # Return the response data
    return response.json()
app.include_image(ImagePrompt, prefix="OpenAI API")
#################################################################################
#                                 Network
#################################################################################
network_api_router = APIRouter(tags=["blah"])


@network_api_router.get("/TODO")
def get_network_internet_connectivity() -> Dict[str, bool]:
    """TODO."""
    return {"todo": "todo"}


@network_api_router.get("/yoyo")
def get_general_network_state() -> Dict[str, Any]:
    """TODO."""
    return {"todo": "todo"}

app.include_router(network_api_router, prefix="/blah")


#################################################################################
#                                 WiFi
#################################################################################
wifi_api_router = APIRouter(tags=["todo2"])


@wifi_api_router.post("/todo")
@app.state.limiter.limit("1/second")
def post_wifi_toggle(status: bool, request: Request) -> Dict[str, Any]:
    """TODO."""
    # success, error_message = wifi.wifi_toggle(status)
    return {
        "success": True,
        "error_message": "TODO",
    }

app.include_router(wifi_api_router, prefix="/todo")
