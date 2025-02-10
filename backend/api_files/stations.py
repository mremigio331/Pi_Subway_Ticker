import additional_py_files.constants as constants
import additional_py_files.common as common
from api_files.models import UpdateStationModel, ForceChangeStationModel

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
    "/all_stations",
    summary="Get All Train Stations",
    response_description="List of all train stations",
)
async def get_all_train_stations(request: Request):
    try:
        all_train_stations = common.stations_load_v2()
        all_stations_list = list(all_train_stations.keys())
        logger.info("All train stations list retrieved successfully")
        return JSONResponse(content=all_stations_list, status_code=200)
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
    "/specific_station/enabled_status",
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


@router.get(
    "/current_station",
    summary="Get Current Station",
    response_description="Current station information",
)
async def get_current_station():
    try:
        logger.debug("Opening API export file to get current station data")
        all_trains_data = common.open_json_file(constants.API_EXPORT_FILE)
        logger.debug(f"All trains data: {all_trains_data}")
        current_station = {
            constants.CURRENT_STATION: all_trains_data[constants.CURRENT_STATION]
        }
        logger.info("Current station data retrieved successfully")
        return JSONResponse(content=current_station, status_code=200)
    except Exception as e:
        error = str(e)
        logger.error(f"Error occurred while retrieving current station data: {error}")
        raise HTTPException(status_code=500, detail=error)


@router.put(
    "/current_station",
    summary="Update Current Station",
    response_description="Update current station information",
)
async def update_current_station(body: UpdateStationModel):
    station = body.station
    cycle = body.cycle

    try:
        logger.debug("Opening API export file to update current station data")
        all_trains_data = common.open_json_file(constants.API_EXPORT_FILE)
        all_config = common.open_json_file(constants.CONFIG_FILE)
        current_station = all_trains_data[constants.CURRENT_STATION]
        current_cycle = all_config[constants.CYCLE]
        new_cycle = cycle

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
        if current_station == station and new_cycle == current_cycle:
            message = f"Configs are already set to current_station {current_station} cycle: {new_cycle}. No changes made"
            logger.debug(message)
            return JSONResponse(content=message, status_code=204)

        all_config[constants.STATION] = station
        all_config[constants.CYCLE] = new_cycle
        message = f"Successfully updated the current station to {station} and cycle to {new_cycle}."

        common.update_json(constants.CONFIG_FILE, all_config)
        logger.info(message)
        return JSONResponse(content=message, status_code=200)

    except Exception as e:
        error = str(e)
        logger.error(f"Error occurred while updating current station data: {error}")
        raise HTTPException(status_code=500, detail=error)


@router.put(
    "/force_change_station",
    summary="Force Change Station",
    response_description="Force change station information",
)
async def force_change_station(request: ForceChangeStationModel):
    force_change_station = request.force_change_station
    cycle = request.cycle

    try:
        logger.debug("Opening API export file to update force change station data")
        all_trains_data = common.open_json_file(constants.API_EXPORT_FILE)
        all_config = common.open_json_file(constants.CONFIG_FILE)
        current_station = all_trains_data[constants.CURRENT_STATION]
        current_cycle = all_config[constants.CYCLE]
        new_cycle = cycle

        if not common.station_check_v2(force_change_station):
            logger.error(
                f"{force_change_station} not found. Ensure you are using the stop name with the stop id"
            )
            return JSONResponse(
                content={
                    "error": f"{force_change_station} not found. Ensure you are using the stop name with the stop id"
                },
                status_code=404,
            )
        if current_station == force_change_station and new_cycle == current_cycle:
            message = f"Configs are already set to current_station {current_station} cycle: {new_cycle}. No changes made"
            logger.debug(message)
            return JSONResponse(content=message, status_code=204)

        all_config[constants.FORCE_CHANGE_STATION] = force_change_station
        all_config[constants.CYCLE] = new_cycle
        message = f"Successfully updated the force_change to {force_change_station} and cycle to {new_cycle}."

        common.update_json(constants.CONFIG_FILE, all_config)
        logger.info(message)
        return JSONResponse(content=message, status_code=200)

    except Exception as e:
        error = str(e)
        logger.error(
            f"Error occurred while updating force change station data: {error}"
        )
        raise HTTPException(status_code=500, detail=error)
