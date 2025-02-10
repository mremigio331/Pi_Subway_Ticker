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
    "/",
    summary="Get All Configs",
    response_description="List of all configurations",
)
async def get_all_configs():
    try:
        all_config = common.open_json_file(constants.CONFIG_FILE)
        config_list = common.dict_to_list_of_dicts(all_config)
        logger.info("All configurations retrieved successfully")
        return JSONResponse(content=config_list, status_code=200)
    except Exception as e:
        error = str(e)
        logger.error(f"Error occurred: {error}")
        raise HTTPException(status_code=500, detail=error)


@router.get(
    "/{config}",
    summary="Get Specific Config",
    response_description="Get a specific configuration",
)
async def specific_config(config: str):
    try:
        all_config = common.open_json_file(constants.CONFIG_FILE)
        return_dict = {"requested_config": config, "value": all_config[config]}
        logger.info(f"Configuration {config} retrieved successfully")
        return JSONResponse(content=return_dict, status_code=200)
    except Exception as e:
        error = str(e)
        logger.error(f"Error occurred: {error}")
        raise HTTPException(status_code=500, detail=error)


@router.put(
    "/{config}",
    summary="Update Specific Config",
    response_description="Update a specific configuration",
)
async def update_specific_config(
    config: str,
    value: str = Query(..., description="The new value for the configuration"),
):
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
        else:
            message = (
                f"Config {config} has been updated from {current_value} to {new_value}"
            )

        all_configs[config] = new_value
        common.update_json(constants.CONFIG_FILE, all_configs)
        logger.info(message)
        return JSONResponse(content=message, status_code=200)

    except Exception as e:
        error = str(e)
        logger.error(f"Error occurred: {error}")
        raise HTTPException(status_code=500, detail=error)
