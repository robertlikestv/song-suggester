"""Client for accessing Last.fm API data.

Provides an integration wrapper around PyLast to handle API authentication,
fetching artist tags/genres, and querying track recommendations.
"""

import logging
from typing import Optional
import pylast
from app.config import settings

logger = logging.getLogger(__name__)


class LastfmService:
    """Last.fm API Client wrapper."""

    def __init__(self) -> None:
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
        except Exception as err:
            logger.error("Failed to fetch genres for artist '%s': %s", artist, err)
            return []

    def get_similar_track(self, artist: str, title: str) -> Optional[tuple[str, str]]:
        """Finds the top similar track recommendation for a given song.

        Args:
            artist: Name of the artist.
            title: Title of the track.

        Returns:
            A tuple of (similar_artist, similar_title) if found, or None if no match exists.
        """
        try:
            similar_items = self.network.get_track(artist, title).get_similar(limit=1)

            if not similar_items:
                logger.warning("No similar tracks found for '%s - %s'", artist, title)
                return None

            top_match = similar_items[0].item
            similar_artist = top_match.get_artist().get_name()
            similar_title = top_match.get_title()

            return (similar_artist, similar_title)
        except Exception as err:
            logger.error("Failed to fetch similar track for '%s - %s': %s", artist, title, err)
            return None


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger.info("Initializing LastfmService...")
    service = LastfmService()
    genres = service.get_artist_genres("Radiohead")
    logger.info("Retrieved genres: %s", genres)