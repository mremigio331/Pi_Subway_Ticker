from pydantic import BaseModel


class UpdateStationModel(BaseModel):
    station: str
    cycle: bool


class ForceChangeStationModel(BaseModel):
    force_change_station: str
    cycle: bool
