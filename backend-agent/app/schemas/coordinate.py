from pydantic import BaseModel, HttpUrl

class ScrapeRequest(BaseModel):
    url: HttpUrl  # Using HttpUrl ensures the user provides a real website link