"""
Client for accessing Last.fm API data.
"""
import pylast

from app.config import Settings
from app.schemas import Track


class LastfmClient:
    """Last.fm API Client wrapper."""

    def __init__(self, api_key = str, api_secret = str) -> None:
        """Initializes connection to Last.fm API network."""
        self.network = pylast.LastFMNetwork(
            api_key=api_key,
            api_secret=api_secret,
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


    def get_similar_tracks(
        self, 
        artist: str, 
        title: str, 
        limit=10,
        max_listeners: int = 500_000
    ) -> list[Track] | None:
        """Finds the top similar track recommendation for a given song.

        Args:
            artist: Name of the artist.
            title: Title of the track.
            limit: Maximum number of songs to be returned. Defaults to 10

        Returns:
            A tuple of (similar_artist, similar_title) if found, or None 
                if no match exists.
        """
        # Will be actively filtering out poor results, so need to query
        # for a few extra 
        fetch_buffer = max(limit * 3, 50)
        try:
            seed_track = self.network.get_track(artist, title)
            similar_items = seed_track.get_similar(limit=fetch_buffer)
        except pylast.PyLastError:
            return []
        
        found_tracks: list[Track] = []
        seen_tracks: set[str] = set()

        # Want to avoid having the initial song be recommended
        seed_key = (
            f"{artist.lower().strip()} - {title.lower().strip()}"
        )
        seen_tracks.add(seed_key)

        for item in similar_items:
            found_track = item.item
            found_artist = found_track.get_artist().get_name()
            found_title = found_track.get_title()
            track_key = (
                f"{found_artist.lower().strip()} - {found_title.lower().strip()}"
            )

            if track_key in seen_tracks:
                continue

            try:
                listener_count = found_track.get_listener_count()
            except pylast.PyLastError:
                continue

            # Want to avoid overly popular songs
            if listener_count > max_listeners:
                continue

            new_track = Track(
                title=found_title, 
                artist=found_artist,
                listeners=listener_count,
                playcount=found_track.get_playcount()
            )
            found_tracks.append(new_track)

            if len(found_tracks) == limit:
                break

        return found_tracks


if __name__ == "__main__":
    settings = Settings()
    service = LastfmClient(settings)
    tracks = service.get_similar_tracks(
        artist="Radiohead", 
        title="Weird Fishes/Arpeggi"
    )
    print(tracks)