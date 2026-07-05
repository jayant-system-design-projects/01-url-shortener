from pydantic import BaseModel, HttpUrl


class CreateShortenURLRequest(BaseModel):
    url: HttpUrl
