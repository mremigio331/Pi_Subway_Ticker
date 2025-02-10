from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/", summary="Home Endpoint", response_description="Welcome message")
async def pi_api_home():
    try:
        welcome_message = (
            "Welcome to the locally hosted endpoint " + "for your Pi Subway Tracker"
        )
        logger.info("Welcome message sent successfully")
        return JSONResponse(content={"message": welcome_message}, status_code=200)

    except Exception as e:
        error = str(e)
        logger.error(f"Error occurred: {error}")
        raise HTTPException(status_code=500, detail=error)
