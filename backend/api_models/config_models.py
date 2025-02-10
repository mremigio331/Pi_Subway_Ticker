from pydantic import BaseModel, Field


class UpdateConfigModel(BaseModel):
    config: str = Field(..., description="The configuration key to update")
    value: str = Field(..., description="The new value for the configuration")
