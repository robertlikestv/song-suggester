"""
Client for accessing Spotify Web API data.
"""

import json
from pprint import pprint
import logging
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# local
from app.config import Settings
from app.schemas import Track


class SpotifyClient:
    """Creates a Spotify API Client wrapper."""

    """def __init__(self, settings: Settings):"""
    def __init__(self, auth_token: str):
        """Authorizes connection to Spotify API via OAuth 2.0."""
        """scope = "user-top-read"

        self._client = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=settings.SPOTIFY_CLIENT_ID,
                client_secret=settings.SPOTIFY_CLIENT_SECRET,
                redirect_uri=settings.SPOTIFY_REDIRECT_URI,
                scope=scope,
                cache_handler=None,
                show_dialog=True

            )
        )"""
        self._client = spotipy.Spotify(auth=auth_token)


    def get_top_tracks(
            self, 
            limit = 20, 
            offset = 0, 
            time_range = "medium_term"
            ) -> list[Track]:
        """Fetch and format user's top tracks.

        Args:
            limit: Number of tracks to return. Defaults to 20.
            offset: Number of top tracks to skip over. Defaults to 0.
            time_range: Period of time to analyze ("short_term", "medium_term", "long_term").
        """
        response = self._client.current_user_top_tracks(
            limit=limit, 
            offset=offset, 
            time_range=time_range
        )
        
        tracks = []
        for item in response.get("items", []):
            tracks.append(Track(
                title=item["name"],
                artist=item["artists"][0]["name"],
                spotify_uri=item["uri"],
                spotify_url=item["external_urls"].get("spotify")
            ))
        return tracks
    

if __name__ == "__main__":
    settings = Settings()
    client = SpotifyClient(settings)
    tracks = client.get_top_tracks()
    pprint(tracks)
   