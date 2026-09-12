"""
Client for accessing Spotify Web API data.

Provides an integration wrapper around Spotipy to handle OAuth authentication
and fetch user top tracks and associated metadata.
"""

import json
import logging
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from app.config import Settings


class SpotifyClient:
    """Creates a Spotify API Client wrapper."""

    def __init__(self, settings: Settings) -> None:
        """Authorizes connection to Spotify API via OAuth 2.0."""
        scope = "user-top-read"

        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=settings.SPOTIFY_CLIENT_ID,
                client_secret=settings.SPOTIFY_CLIENT_SECRET,
                redirect_uri=settings.SPOTIFY_REDIRECT_URI,
                scope=scope,
            )
        )


    def get_top_tracks(self, limit: int = 20, offset: int = 0, 
                       time_range: str = "medium_term") -> dict:
        """Fetches the user's top played tracks payload from Spotify.

        Args:
            limit: Number of tracks to return. Defaults to 20.
            offset: Number of top tracks to skip over. Defaults to 0.
            time_range: Period of time to analyze ("short_term", "medium_term", "long_term").

        Returns:
            A dictionary payload containing track items and pagination metadata.
        """
        return self.sp.current_user_top_tracks(limit=limit, offset=offset, time_range=time_range)


    def extract_artists(self, top_tracks_payload: dict) -> list[str]:
        """Extracts primary artist names from a top tracks API payload."""
        artists = []
        for item in top_tracks_payload.get("items", []):
            if item.get("artists"):
                artists.append(item["artists"][0]["name"])
        return artists


    def extract_titles(self, top_tracks_payload: dict) -> list[str]:
        """Extracts track titles from a top tracks API payload."""
        return [item["name"] for item in top_tracks_payload.get("items", [])]


if __name__ == "__main__":
    settings = Settings()
    client = SpotifyClient(settings)
    tracks_data = client.get_top_tracks(time_range="medium_term")

    # Local inspection output
    for idx, (artist, title) in enumerate(
        zip(client.extract_artists(tracks_data), client.extract_titles(tracks_data)), 1
    ):
        print(f"{idx}. {artist} - {title}")