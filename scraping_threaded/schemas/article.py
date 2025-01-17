from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum
from schemas.results import ScrapingResult


class Status(str, Enum):
    """Processing status"""

    UNPROCESSED = "UNPROCESSED"
    CONTENT_FETCHED = "CONTENT-FETCHED"
    CONTENT_EXTRACTED = "CONTENT-EXTRACTED"
    DENYLISTED = "DENYLISTED"
    FAILED = "FAILED"


class Metadata(BaseModel):
    date_guess_method: Optional[dict] = None
    extractor_version: Optional[dict] = None
    geocoder_version: Optional[dict] = None
    nyt_themes_version: Optional[dict] = None


class Article(BaseModel):

    # -- Mediacloud Fields --

    ap_syndicated: Optional[bool]
    collect_date: Optional[str]
    feeds: Optional[str] = None
    guid: Optional[str]
    lang: Optional[str] = "unspecified"
    media_id: Optional[int]
    media_name: Optional[str]
    media_url: Optional[str]
    processed_stories_id: Optional[int]
    publish_date: Optional[str] = None
    stories_id: Optional[int]
    story_tags: Optional[List[dict]] = []
    title: Optional[str]
    url: Optional[str]
    word_count: Optional[int] = None
    metadata: Optional[Metadata]

    # -- Additional Fields --
    batch_id: int = Field(description="Batch identifier")
    imported_from: str = Field(
        default="unspecified", description="Imported from this file")
    imported_at: datetime = Field(default_factory=datetime.now)
    scraping_result: Optional[ScrapingResult] = Field(
        default=None, description="Scraping result")

    # -- Processing Status --

    status: str = Field(default=Status.UNPROCESSED,
                        description="processing status")
    tries: int = Field(default=0, description="number of scraping tries")

    # -- Processing Status --

    def __init__(self, **data):

        # Field cannot be named "language" because
        # of how mongodb handles indexing text fields
        data["lang"] = data["language"]
        super().__init__(**data)
