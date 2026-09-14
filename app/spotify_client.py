"""
Client for accessing Spotify Web API data.
"""

import json
import logging
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# local
from app.config import Settings
from app.models import Track


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
                cache_handler=None,
                show_dialog=True

            )
        )


    def fetch_top_tracks_info(
            self, 
            limit: int = 20, 
            offset: int = 0, 
            time_range: str = "medium_term"
        ) -> dict:
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


def get_top_tracks(
        client: SpotifyClient, 
        limit = 20, 
        offset = 0, 
        time_range = "medium_term"
        ) -> list[Track]:
    """Fetch and format user's top tracks"""
    tracks_data = client.fetch_top_tracks_info(limit, offset, time_range)

    # Artists and titles synced by index
    artists = client.extract_artists(tracks_data)
    titles = client.extract_titles(tracks_data)

    tracks = []
    for (artist, title) in (zip(artists, titles)):
        track = Track(title=title, artist=artist)
        tracks.append(track)

    return tracks


if __name__ == "__main__":
    settings = Settings()
    client = SpotifyClient(settings)
    tracks = get_top_tracks(client)
    print(tracks)
   