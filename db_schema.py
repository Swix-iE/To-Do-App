from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class ToDOModel(BaseModel):
    id : str = Field(alias="_id")
    name : str
    description: str
    is_completed : bool
    created_date : datetime
    updated_date : datetime

    model_config = ConfigDict(populate_by_name=True)
