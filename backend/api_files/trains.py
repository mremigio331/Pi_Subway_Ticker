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
    "/current_station",
    summary="Get Current Station",
    response_description="Current station information",
)
async def get_current_station():
    try:
        all_trains_data = common.open_json_file(constants.API_EXPORT_FILE)
        print(all_trains_data)
        current_station = {
            constants.CURRENT_STATION: all_trains_data[constants.CURRENT_STATION]
        }
        logger.info("Current station data retrieved successfully")
        return JSONResponse(content=current_station, status_code=200)
    except Exception as e:
        error = str(e)
        logger.error(f"Error occurred: {error}")
        raise HTTPException(status_code=500, detail=error)


@router.put(
    "/current_station",
    summary="Update Current Station",
    response_description="Update current station information",
)
async def update_current_station(
    station: str = Query(None, description="The station name with the stop id"),
    force_change_station: str = Query(
        None, description="The force change station name with the stop id"
    ),
    cycle: bool = Query(..., description="The cycle status"),
):
    if not station and not force_change_station:
        logger.error(
            "Header is missing one of the following: station or force_change_station"
        )
        return JSONResponse(
            content={
                "error": "Header is missing one of the following: station or force_change_station"
            },
            status_code=400,
        )

    if station and force_change_station:
        logger.error(
            "Can only pass one of the following headers: station or force_change_station"
        )
        return JSONResponse(
            content={
                "error": "Can only pass one of the following headers: station or force_change_station"
            },
            status_code=400,
        )

    try:
        all_trains_data = common.open_json_file(constants.API_EXPORT_FILE)
        all_config = common.open_json_file(constants.CONFIG_FILE)
        current_station = all_trains_data[constants.CURRENT_STATION]
        current_cycle = all_config[constants.CYCLE]
        new_cycle = cycle

        if station:
            new_station = station
            if not common.station_check_v2(new_station):
                logger.error(
                    f"{new_station} not found. Ensure you are using the stop name with the stop id"
                )
                return JSONResponse(
                    content={
                        "error": f"{new_station} not found. Ensure you are using the stop name with the stop id"
                    },
                    status_code=404,
                )
            if current_station == new_station and new_cycle == current_cycle:
                message = f"Configs are already set to current_station {current_station} cycle: {new_cycle}. No changes made"
                return JSONResponse(content=message, status_code=204)

        elif force_change_station:
            new_station = force_change_station
            if not common.station_check_v2(new_station):
                logger.error(
                    f"{new_station} not found. Ensure you are using the stop name with the stop id"
                )
                return JSONResponse(
                    content={
                        "error": f"{new_station} not found. Ensure you are using the stop name with the stop id"
                    },
                    status_code=404,
                )
            if current_station == new_station and new_cycle == current_cycle:
                message = f"Configs are already set to current_station {current_station} cycle: {new_cycle}. No changes made"
                return JSONResponse(content=message, status_code=204)

        if station:
            all_config[constants.STATION] = new_station
            all_config[constants.CYCLE] = new_cycle
            message = f"Successfully updated the current station to {new_station} and cycle to {new_cycle}."

        elif force_change_station:
            all_config[constants.FORCE_CHANGE_STATION] = new_station
            all_config[constants.CYCLE] = new_cycle
            message = f"Successfully updated the force_change to {new_station} and cycle to {new_cycle}."

        common.update_json(constants.CONFIG_FILE, all_config)
        logger.info(message)
        return JSONResponse(content=message, status_code=200)

    except Exception as e:
        error = str(e)
        logger.error(f"Error occurred: {error}")
        raise HTTPException(status_code=500, detail=error)


@router.get(
    "/next_four",
    summary="Get Next Four Trains",
    response_description="Next four trains information",
)
async def get_next_four():
    try:
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
        logger.error(f"Error occurred: {error}")
        raise HTTPException(status_code=500, detail=error)


@router.get(
    "/all_data", summary="Get All Trains Data", response_description="All trains data"
)
async def get_all_trains_data():
    try:
        all_trains_data = common.open_json_file(constants.API_EXPORT_FILE)
        logger.info("All trains data retrieved successfully")
        return JSONResponse(content=all_trains_data, status_code=200)
    except Exception as e:
        error = str(e)
        logger.error(f"Error occurred: {error}")
        raise HTTPException(status_code=500, detail=error)
