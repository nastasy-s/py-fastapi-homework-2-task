from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, field_validator


class CountrySchema(BaseModel):
    id: int
    code: str
    name: Optional[str] = None

    class Config:
        from_attributes = True


class GenreSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class ActorSchema(BaseModel):
    id: int
    name: str

    class Config:

        from_attributes = True


class LanguageSchema(BaseModel):
    id: int
    name: str

    class Config:

        from_attributes = True


class MovieListItemSchema(BaseModel):
    id: int
    name: str
    date: date
    score: float
    overview: str

    class Config:
        from_attributes = True


class MovieListResponseSchema(BaseModel):
    movies: list[MovieListItemSchema]
    prev_page: Optional[str]
    next_page: Optional[str]
    total_pages: int
    total_items: int


class MovieDetailSchema(BaseModel):
    id: int
    name: str
    date: date
    score: float
    overview: str
    status: str
    budget: float
    revenue: float
    country: Optional[CountrySchema] = None
    genres: list[GenreSchema] = []
    actors: list[ActorSchema] = []
    languages: list[LanguageSchema] = []

    class Config:
        from_attributes = True


class MovieCreateSchema(BaseModel):
    name: str
    date: date
    score: float
    overview: str
    status: str
    budget: float
    revenue: float
    country: str
    genres: list[str] = []
    actors: list[str] = []
    languages: list[str] = []

    @field_validator("name")
    @classmethod
    def name_max_length(cls, v):
        if len(v) > 255:
            raise ValueError("name must not exceed 255 characters")
        return v

    @field_validator("date")
    @classmethod
    def date_not_too_far_future(cls, v):
        now = datetime.now()
        limit = date(now.year + 1, now.month, now.day)
        if v > limit:
            raise ValueError("date must not be more than one year in the future")
        return v

    @field_validator("score")
    @classmethod
    def score_range(cls, v):
        if not (0 <= v <= 100):
            raise ValueError("score must be between 0 and 100")
        return v

    @field_validator("budget", "revenue")
    @classmethod
    def non_negative(cls, v):
        if v < 0:
            raise ValueError("must be non-negative")
        return v

    @field_validator("status")
    @classmethod
    def valid_status(cls, v):
        if v not in {"Released", "Post Production", "In Production"}:
            raise ValueError("invalid status")
        return v


class MovieUpdateSchema(BaseModel):
    name: Optional[str] = None
    date: Optional[date] = None
    score: Optional[float] = None
    overview: Optional[str] = None
    status: Optional[str] = None
    budget: Optional[float] = None
    revenue: Optional[float] = None

    @field_validator("score")
    @classmethod
    def score_range(cls, v):
        if v is not None and not (0 <= v <= 100):
            raise ValueError("score must be between 0 and 100")
        return v

    @field_validator("budget", "revenue")
    @classmethod
    def non_negative(cls, v):
        if v is not None and v < 0:
            raise ValueError("must be non-negative")
        return v

    @field_validator("status")
    @classmethod
    def valid_status(cls, v):
        if v is not None and v not in {"Released", "Post Production", "In Production"}:
            raise ValueError("invalid status")
        return v
