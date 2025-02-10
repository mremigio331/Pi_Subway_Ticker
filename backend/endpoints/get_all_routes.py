from endpoints.home import router as home_router
from endpoints.configs import router as configs_router
from endpoints.stations import router as stations_router
from endpoints.trains import router as trains_router
from endpoints.system import router as system_router


def get_all_routes(app):
    # Home
    # Get
    app.include_router(home_router, tags=["General"])

    # Configs
    # Get and Put
    app.include_router(configs_router, prefix="/configs", tags=["Configs"])

    # Stations
    # Get and Put
    app.include_router(stations_router, prefix="/stations", tags=["Stations"])

    # Trains
    # Get and Put
    app.include_router(trains_router, prefix="/trains", tags=["Trains"])

    # System
    # Post
    app.include_router(system_router, prefix="/system", tags=["System"])

    return app
