import spotipy
import httpx
from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.responses import RedirectResponse
from spotipy.oauth2 import SpotifyOAuth

from app.config import Settings, get_settings
from app.lastfm_client import LastfmClient
from app.spotify_client import SpotifyClient
from app.schemas import RecommendationRequest, RecommendationResponse
from app.services import recommend_tracks


app = FastAPI()


@app.get("/login")
def login(settings: Settings = Depends(get_settings)):
    sp_oauth = SpotifyOAuth(
        client_id=settings.SPOTIFY_CLIENT_ID,
        client_secret=settings.SPOTIFY_CLIENT_SECRET,
        redirect_uri=settings.SPOTIFY_REDIRECT_URI,
        scope="user-top-read"
    )

    auth_url = sp_oauth.get_authorize_url()
    return RedirectResponse(auth_url)


@app.get("/callback")
def callback(code: str, settings: Settings = Depends(get_settings)):
    sp_oauth = SpotifyOAuth(
        client_id=settings.SPOTIFY_CLIENT_ID,
        client_secret=settings.SPOTIFY_CLIENT_SECRET,
        redirect_uri=settings.SPOTIFY_REDIRECT_URI
    )
    token_info = sp_oauth.get_access_token(code)

    return {"access_token": token_info["access_token"]}


def get_lastfm_client(
        settings: Settings = Depends(get_settings)
    ) -> LastfmClient:
    """Get a LastFM Client from environment variables.
    """
    return LastfmClient(
        api_key=settings.LASTFM_API_KEY,
        api_secret=settings.LASTFM_API_SECRET
    )


def get_spotify_client(payload: RecommendationRequest) -> SpotifyClient:
    """Get a Spotify client from a passed payload.
    """
    return SpotifyClient(auth_token=payload.spotify_token)


@app.post(
    "/api/v1/recommendations",
    response_model=RecommendationResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate song recommendations",
    tags=["Recommendations"]
)
def get_recommendations(
    payload: RecommendationRequest,
    spotify_client: SpotifyClient = Depends(get_spotify_client),
    lastfm_client: LastfmClient = Depends(get_lastfm_client)
) -> RecommendationResponse:
    try:
        recommendations = recommend_tracks(
            spotify_client=spotify_client,
            lastfm_client=lastfm_client,
            variance=payload.variance,
            offset=payload.offset,
            time_range=payload.time_range,
            limit=payload.limit,
            max_listeners=payload.max_listeners,
            max_tracks_per_artist=payload.max_tracks_per_artist
        )

        return RecommendationResponse(
            total=len(recommendations),
            seed_tracks_used=payload.variance,
            recommendations=recommendations
        )
    except spotipy.SpotifyException as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Spotify authentication failed: {err.msg}"
        ) from err
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Failed to generate recommendations: {str(err)}"
        ) from err


@app.get("/healthz", status_code=status.HTTP_200_OK, tags=["Monitoring"])
async def health_check() -> dict[str, str]:
    return {"status": "healthy"}