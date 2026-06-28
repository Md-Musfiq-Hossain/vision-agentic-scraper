from pydantic import BaseModel, HttpUrl
from typing import Optional

class ScrapeRequest(BaseModel):
    url: HttpUrl
    target_element: Optional[str] = None