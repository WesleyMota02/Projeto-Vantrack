from datetime import datetime
from pydantic import BaseModel, validator

class LocalizacaoGPS(BaseModel):
    id: int = None
    latitude: float
    longitude: float
    timestamp: datetime
    veiculo_id: int

    @validator('latitude')
    def validar_latitude(cls, v):
        if not (-90 <= v <= 90):
            raise ValueError('Latitude deve estar entre -90 e 90')
        return v

    @validator('longitude')
    def validar_longitude(cls, v):
        if not (-180 <= v <= 180):
            raise ValueError('Longitude deve estar entre -180 e 180')
        return v

    class Config:
        from_attributes = True

class LocalizacaoGPSCreate(BaseModel):
    latitude: float
    longitude: float
    veiculo_id: int

    @validator('latitude')
    def validar_latitude(cls, v):
        if not (-90 <= v <= 90):
            raise ValueError('Latitude deve estar entre -90 e 90')
        return v

    @validator('longitude')
    def validar_longitude(cls, v):
        if not (-180 <= v <= 180):
            raise ValueError('Longitude deve estar entre -180 e 180')
        return v
