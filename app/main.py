"""Server routes defintioins."""

from typing import Any, Dict, List

from fastapi import APIRouter, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.core.fastapi_config import Settings
from app.core.logs.logs import Logs
from app.core.utility.logger_setup import get_logger
from app.core.utility.timing_middleware import TimingMiddleware
from data_models import InstagramInput

log = get_logger()


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
#                                 Network
#################################################################################
network_api_router = APIRouter(tags=["Testing"])


@network_api_router.get("/TODO")
def get_network_internet_connectivity() -> Dict[str, bool]:
    """TODO."""
    return {"todo": "todo"}


@network_api_router.get("/TODO")
def get_general_network_state() -> Dict[str, Any]:
    """TODO."""
    return {"todo": "todo"}

@network_api_router.get("/MYTEST")
def get_my_test_info() -> Dict[str, Any]:
    #"""TODO."""
    return {"todo": "todo"}

@network_api_router.post("/instagram")
def get_my_test_info(jsonInput) -> Dict[str, Any]:
    
    # parse info into object
    instagramInput = InstagramInput(jsonInput)

    # object has custinput, prompt for image
    # pass info to insta
    return {"todo": "todo"}

app.include_router(network_api_router, prefix="/network")


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
