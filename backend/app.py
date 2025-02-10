import logging
from logging.handlers import TimedRotatingFileHandler
from endpoints.get_all_routes import get_all_routes
import os
import uvicorn
import sys
import additional_py_files.constants as constants
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

sys.dont_write_bytecode = True
# Setup logging
LOG_DIR = "/var/log/subway_ticker"
LOG_FILE_API = os.path.join(LOG_DIR, "api.log")
logger = logging.getLogger("trains_api")
logger.setLevel(logging.INFO)


def setup_logging():
    """Ensure the log directory exists and set up logging handlers."""
    try:
        if not os.path.exists(LOG_DIR):
            os.makedirs(LOG_DIR)
            logger.info(f"Log directory created at {LOG_DIR}.")
    except Exception as e:
        raise SystemExit(f"Critical error: Unable to create log directory: {e}")

    # File Handler
    file_handler = TimedRotatingFileHandler(
        LOG_FILE_API, when="midnight", backupCount=7
    )
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    )
    file_handler.suffix = "%Y-%m-%d"

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    )

    # Add handlers if not already present
    if not logger.hasHandlers():
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)


setup_logging()

app = FastAPI(
    title="Pi Subway Ticker",
    description="API for the Pi Subway Ticker",
    version="1.0.0",
)


@app.middleware("http")
async def log_request_info(request: Request, call_next):
    client_host = request.client.host
    request_method = request.method
    request_url = request.url.path
    headers = dict(request.headers)

    body = await request.body()
    payload = body.decode("utf-8") if body else "{}"

    logger.info(
        f"Incoming request from {client_host}: {request_method} {request_url}, "
        f"Payload: {payload}"
    )

    response = await call_next(request)

    logger.info(
        f"Response for {request_method} {request_url} from {client_host}: "
        f"Status code: {response.status_code}"
    )

    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logger.info("CORS configured for local development (open for all origins).")

app = get_all_routes(app)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=5000, log_level="info", reload=True)
