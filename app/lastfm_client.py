"""
Client for accessing Last.fm API data.
"""

import pylast
import json

# local
from app.config import Settings
from app.models import Track


class LastfmClient:
    """Last.fm API Client wrapper."""

    def __init__(self, settings: Settings) -> None:
        """Initializes connection to Last.fm API network."""
        self.network = pylast.LastFMNetwork(
            api_key=settings.LASTFM_API_KEY,
            api_secret=settings.LASTFM_API_SECRET,
        )

    def get_artist_genres(self, artist: str, limit: int = 3) -> list[str]:
        """Gets top genres/tags associated with an artist.

        Args:
            artist: Name of the artist to query.
            limit: Maximum number of genre tags to return. Defaults to 3.

        Returns:
            A list of title-cased genre names.
        """
        try:
            raw_artist_tags = self.network.get_artist(artist).get_top_tags()

            tags = []
            for tag in raw_artist_tags[:limit]:
                tags.append(tag.item.get_name().title())

            return tags
        except Exception:
            return []

    def get_similar_tracks(self, artist: str, title: str, 
                           limit=10) -> list[Track] | None:
        """Finds the top similar track recommendation for a given song.

        Args:
            artist: Name of the artist.
            title: Title of the track.
            limit: Maximum number of songs to be returned. Defaults to 10

        Returns:
            A tuple of (similar_artist, similar_title) if found, or None 
                if no match exists.
        """
        try:
            similar_items = self.network.get_track(artist, title).get_similar(limit)

            if not similar_items:
                return None

            tracks = []
            for item in similar_items:
                found_track = item.item
                similar_artist = found_track.get_artist().get_name()
                similar_title = found_track.get_title()

                new_track = Track(similar_title, similar_artist)
                tracks.append(new_track)
            return tracks
        except KeyError:
            return None


if __name__ == "__main__":
    settings = Settings()
    service = LastfmClient(settings)
    tracks = service.get_similar_tracks(
        artist="Radiohead", 
        title="Weird Fishes/Arpeggi"
    )
    print(tracks)