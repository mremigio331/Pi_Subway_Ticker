import additional_py_files.constants as constants
import additional_py_files.common as common

from fastapi import APIRouter, HTTPException, Request, Query
from fastapi.responses import JSONResponse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.get(
    "/full_info",
    summary="Get All Train Stations",
    response_description="List of all train stations",
)
async def get_all_train_stations(request: Request):
    try:
        all_train_stations = common.stations_load_v2()
        logger.info("All train stations data retrieved successfully")
        return JSONResponse(content=all_train_stations, status_code=200)
    except Exception as e:
        error = str(e)
        logger.error(f"Error occurred: {error}")
        raise HTTPException(status_code=500, detail=error)


@router.get(
    "/specific_station",
    summary="Get Specific Station Info",
    response_description="Information of a specific train station",
)
async def specific_station_info(
    station: str = Query(..., description="The station name with the stop id")
):
    try:
        if not common.station_check_v2(station):
            logger.error(
                f"{station} not found. Ensure you are using the stop name with the stop id"
            )
            return JSONResponse(
                content={
                    "error": f"{station} not found. Ensure you are using the stop name with the stop id"
                },
                status_code=404,
            )

        all_train_stations = common.stations_load_v2()
        logger.info(f"Data for station {station} retrieved successfully")
        return JSONResponse(content=all_train_stations[station], status_code=200)
    except Exception as e:
        error = str(e)
        logger.error(f"Error occurred: {error}")
        raise HTTPException(status_code=500, detail=error)


@router.put(
    "/specific_station",
    summary="Update Specific Station Info",
    response_description="Update information of a specific train station",
)
async def update_specific_station_info(
    station: str = Query(..., description="The station name with the stop id"),
    enabled: bool = Query(None, description="The enabled status of the station"),
):
    try:
        if not common.station_check_v2(station):
            logger.error(
                f"{station} not found. Ensure you are using the stop name with the stop id"
            )
            return JSONResponse(
                content={
                    "error": f"{station} not found. Ensure you are using the stop name with the stop id"
                },
                status_code=404,
            )

        all_train_stations = common.stations_load_v2()
        highlighted_station = all_train_stations[station]
        if enabled is not None:
            highlighted_station[constants.ENABLED] = enabled
            all_train_stations[station] = highlighted_station
            common.update_json(constants.STATIONS_FILE, all_train_stations)

        return_message = {
            "message": f"Successfully updated {station} station status to {enabled}",
            "updated_data": highlighted_station,
        }
        logger.info(f"Station {station} updated successfully")
        return JSONResponse(content=return_message, status_code=200)
    except Exception as e:
        error = str(e)
        logger.error(f"Error occurred: {error}")
        raise HTTPException(status_code=500, detail=error)
