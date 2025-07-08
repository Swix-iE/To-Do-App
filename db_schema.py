from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

class ToDOCreateModel(BaseModel):
    
    name : Optional[str] = None
    description: Optional[str] = None
    is_completed : Optional[bool] = None
    due_date: Optional[datetime] = None
    

class ToDOUpdateModel(ToDOCreateModel):
    id : str = Field(alias="_id")

class ToDOModel(ToDOCreateModel):
    id : str = Field(alias="_id")
    created_date : Optional[datetime] = None
    updated_date: Optional[datetime] = None

    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders = {
            datetime: lambda d: d.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        )


