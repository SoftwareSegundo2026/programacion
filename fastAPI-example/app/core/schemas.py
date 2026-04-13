from pydantic import BaseModel, ConfigDict
from datetime import datetime

def datetime_to_iso_str(dt: datetime) -> str:
    return dt.isoformat()

class CustomModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={datetime: datetime_to_iso_str},
    )