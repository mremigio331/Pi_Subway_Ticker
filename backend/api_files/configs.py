import additional_py_files.constants as constants
import additional_py_files.common as common
from api_files.config_models import UpdateConfigModel

from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import JSONResponse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.get(
    "/",
    summary="Get All Configs",
    response_description="List of all configurations",
)
async def get_all_configs():
    logger.debug("Request received to get all configurations")
    try:
        all_config = common.open_json_file(constants.CONFIG_FILE)
        config_list = common.dict_to_list_of_dicts(all_config)
        logger.info("All configurations retrieved successfully")
        return JSONResponse(content=config_list, status_code=200)
    except Exception as e:
        error = str(e)
        logger.error(f"Error occurred while retrieving all configurations: {error}")
        raise HTTPException(status_code=500, detail=error)


@router.get(
    "/get_specific_config",
    summary="Get Specific Config",
    response_description="Get a specific configuration",
)
async def specific_config(
    config: str = Query(..., description="The configuration key to retrieve")
):
    logger.debug(f"Request received to get specific configuration: {config}")
    try:
        all_config = common.open_json_file(constants.CONFIG_FILE)
        return_dict = {"requested_config": config, "value": all_config[config]}
        logger.info(f"Configuration {config} retrieved successfully")
        return JSONResponse(content=return_dict, status_code=200)
    except Exception as e:
        error = str(e)
        logger.error(f"Error occurred while retrieving configuration {config}: {error}")
        raise HTTPException(status_code=500, detail=error)


@router.put(
    "/update_specific_config",
    summary="Update Specific Config",
    response_description="Update a specific configuration",
)
async def update_specific_config(
    request: UpdateConfigModel,
):
    config = request.config
    value = request.value
    logger.debug(
        f"Request received to update configuration: {config} to value: {value}"
    )

    try:
        all_configs = common.open_json_file(constants.CONFIG_FILE)
        current_value = all_configs[config]
        new_value = ""

        if config in constants.CONFIG_BOOL_OPTIONS:
            new_value = common.str_to_bool(value)
        else:
            new_value = value

        if current_value == new_value:
            message = f"Config {config} is already set to {new_value}"
            logger.debug(message)
        else:
            message = (
                f"Config {config} has been updated from {current_value} to {new_value}"
            )
            logger.debug(message)

        all_configs[config] = new_value
        common.update_json(constants.CONFIG_FILE, all_configs)
        logger.info(message)
        return JSONResponse(content=message, status_code=200)

    except Exception as e:
        error = str(e)
        logger.error(f"Error occurred while updating configuration {config}: {error}")
        raise HTTPException(status_code=500, detail=error)
