import additional_py_files.constants as constants
import additional_py_files.common as common

from fastapi import APIRouter, HTTPException, Request, Query
from fastapi.responses import JSONResponse
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.get(
    "/next_four",
    summary="Get Next Four Trains",
    response_description="Next four trains information",
)
async def get_next_four():
    try:
        logger.debug("Opening API export file to get next four trains data")
        all_trains_data = common.open_json_file(constants.API_EXPORT_FILE)
        next_four_info = {
            constants.CURRENT_STATION: common.build_station_element(
                all_trains_data[constants.CURRENT_STATION]
            ),
            constants.NEXT_FOUR: all_trains_data[constants.NEXT_FOUR],
            constants.TIMESTAMP: all_trains_data[constants.TIMESTAMP],
            constants.LOADING: all_trains_data[constants.LOADING],
        }
        logger.info("Next four trains data retrieved successfully")
        return JSONResponse(content=next_four_info, status_code=200)
    except Exception as e:
        error = str(e)
        logger.error(f"Error occurred while retrieving next four trains data: {error}")
        raise HTTPException(status_code=500, detail=error)


@router.get(
    "/all_data", summary="Get All Trains Data", response_description="All trains data"
)
async def get_all_trains_data():
    try:
        logger.debug("Opening API export file to get all trains data")
        all_trains_data = common.open_json_file(constants.API_EXPORT_FILE)
        logger.info("All trains data retrieved successfully")
        return JSONResponse(content=all_trains_data, status_code=200)
    except Exception as e:
        error = str(e)
        logger.error(f"Error occurred while retrieving all trains data: {error}")
        raise HTTPException(status_code=500, detail=error)
