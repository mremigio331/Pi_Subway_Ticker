from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/system_restart",
    summary="System Restart",
    response_description="Restart the system",
)
async def system_restart():
    return_dict = {"message": "Not quite ready to restart yet"}
    logger.info("System restart endpoint called")
    return JSONResponse(content=return_dict, status_code=501)

    # try:
    #     subprocess.run(['sudo', 'reboot'])
    #     logger.info("Raspberry Pi is restarting...")
    #     return JSONResponse(content={'message': 'Raspberry Pi is restarting...'}, status_code=200)
    # except Exception as e:
    #     error = str(e)
    #     logger.error(f"Error occurred: {error}")
    #     return JSONResponse(content={'error': error}, status_code=500)


@router.post(
    "/system_update", summary="System Update", response_description="Update the system"
)
async def system_update():
    return_dict = {"message": "Not quite ready to update the system yet"}
    logger.info("System update endpoint called")
    return JSONResponse(content=return_dict, status_code=501)

    # def generate():
    #    command = ["sudo", "apt", "update"]
    #
    #    # Open a subprocess for the command
    #    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    #
    #    # Stream the output of the command line by line
    #    for line in process.stdout:
    #        yield line.strip() + '\n'  # Yield each line of output with a newline character
    #
    # Return a response object that streams the output
    # return Response(stream_with_context(generate()),
    # content_type='text/event-stream')


@router.post(
    "/pi_update", summary="Pi Update", response_description="Update the Raspberry Pi"
)
async def pi_update():
    return_dict = {"message": "Not quite ready to update the pi yet"}
    logger.info("Pi update endpoint called")
    return JSONResponse(content=return_dict, status_code=501)
