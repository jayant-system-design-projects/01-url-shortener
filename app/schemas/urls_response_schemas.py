from pydantic import BaseModel, ConfigDict, HttpUrl, Field
from typing import Optional


class Data(BaseModel):
    shortened_url: HttpUrl = Field(alias="shortenedURL")

    model_config = ConfigDict(populate_by_name=True)


class ErrorDetails(BaseModel):
    error_code: str = Field(alias="errorCode")
    details: str

    model_config = ConfigDict(populate_by_name=True)


class CreateShortenURLResponse(BaseModel):
    status_code: str = Field(alias="statusCode")
    data: Data
    error_details: Optional[ErrorDetails] = Field(alias="errorDetails", default=None)

    model_config = ConfigDict(populate_by_name=True)
