from pydantic import BaseModel, Field, HttpUrl


class Track(BaseModel):
    title: str = Field(..., description="Title of the recommended track")
    artist: str = Field(..., description="Name of the primary artist")
    listeners: int | None = Field(
        default=None,
        ge=0,
        description="Total listener count on Last.fm"
    )
    playcount: int | None = Field(
        default=None,
        ge=0,
        description="Total play count on Last.fm"
    )
    spotify_uri: str | None = Field(
        default=None, 
        description="Spotify track URI used for queuing or adding to playlists"
    )
    spotify_url: HttpUrl | None = Field(
        default=None,
        description="Web link to open track in Spotify"
    )


class RecommendationRequest(BaseModel):
    spotify_token: str = Field(
        ..., 
        description="Active Spotify OAuth access token"
    )
    variance: int = Field(
        default=20,
        ge=1,
        le=20,
        description="Number of top tracks to seed from"
    )
    offset: int = Field(
        default=0,
        ge=0,
        description="Offset for fetching top tracks"
    )
    time_range: str = Field(
        default="medium_term",
        description=(
            "Time window for top tracks ('short_term', "
            "'medium_term', 'long_term')"
        )
    )
    limit: int = Field(
        default=10, 
        ge=1, 
        le=50, 
        description="Total recommendations to return"
    )
    max_listeners: int = Field(
        default=500_000,
        description=(
            "Threshold for filtering out overly popular "
            "music. Listener count is based on LastFM."
        )
    )
    max_tracks_per_artist: int = Field(
        default=2,
        description=(
            "Maximum amount of tracks to be returned by a shared artist."
        )
    )


class RecommendationResponse(BaseModel):
    total: int
    seed_tracks_used: int
    recommendations: list[Track]


    