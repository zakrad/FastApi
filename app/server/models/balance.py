from pydantic import BaseModel, Field


class Balance(BaseModel):
    address: str = Field(...)
    balance: int = Field(..., gt=0)
    value: int = Field(..., gt=0)
    timestamp: int = Field(..., gt=0)
    date: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "address": "0x7a16ff8270133f063aab6c9977183d9e72835428",
                "balance": 200,
                "value": 2000,
                "timestamp": 2032523500,
                "date": "2023-08-17T15:37:23+00:00",
            }
        }
        
def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }