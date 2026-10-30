"""
Recommends songs based on given songs.
"""

from pprint import pprint
from collections import Counter

from app.schemas import Track
from app.config import Settings
from app.spotify_client import SpotifyClient
from app.lastfm_client import LastfmClient

def recommend_tracks(
        spotify_client: SpotifyClient, 
        lastfm_client: LastfmClient,
        variance = 20, 
        offset = 0, 
        time_range = "medium_term",
        limit = 20,
        max_listeners = 500_000,
        max_tracks_per_artist = 1
        ) -> list[Track]:
    """Get user's top tracks and recommend new ones.
    
    Args:
    - variance: Number of user's most listened to tracks 
        to base recommendations off of. Maxes out at 20.
    - limit: Number of recommended tracks to return. Maxes
        out at 200.
    ...
    """
    top_tracks = spotify_client.get_top_tracks(
        limit=variance, 
        offset=offset,
        time_range=time_range,
    )

    if not top_tracks:
        #print("top tracks not returned")
        return []

    seen_tracks: set[str] = set()
    artist_count: Counter[int] = Counter()

    for top_track in top_tracks:
        artist_key = top_track.artist.lower().strip()
        track_key = (
            f"{artist_key}"
            f"- {top_track.title.lower().strip()}"
        )
        
        seen_tracks.add(track_key)
        artist_count[artist_key] += 1

    recommended_tracks_array: list[list[Track]] = []

    for track in top_tracks:
        similar_tracks = lastfm_client.get_similar_tracks(
            artist=track.artist,
            title=track.title,
            limit=limit,
            max_listeners=max_listeners
        )

        if similar_tracks:
            #print(f"similar tracks found for {track}")
            recommended_tracks_array.append(similar_tracks)

    if not recommended_tracks_array:
        #print("no tracks recommended")
        return []

    #print("=========== TOP TRACKS: ===========")
    #pprint(top_tracks)
    #print("=========== RECOMMENDED TRACKS: ===========")
    #pprint(recommended_tracks_array)

    result: list[Track] = []
    max_cols = max(len(row) for row in recommended_tracks_array)

    for col in range(max_cols):
        for row in range(len(recommended_tracks_array)):
            if col >= len(recommended_tracks_array[row]):
                continue

            found_track = recommended_tracks_array[row][col]
            if not found_track:
                continue

            found_artist_key = found_track.artist.lower().strip()
            found_track_key = (
                f"{found_artist_key} - {found_track.title.lower().strip()}"
            )

            if (
                found_track_key in seen_tracks
                or artist_count[found_artist_key] >= max_tracks_per_artist
            ):
                continue

            seen_tracks.add(found_track_key)
            artist_count[found_artist_key] += 1
            result.append(found_track)

            if limit == len(result):
                #print("=========== RESULT: ===========")
                return result

    #print("=========== RESULT: ===========")
    return result


if __name__ == '__main__':
    settings = Settings()
    sp = SpotifyClient(settings)
    lfm = LastfmClient(
        api_key=settings.LASTFM_API_KEY, 
        api_secret=settings.LASTFM_API_SECRET
    )
    pprint(recommend_tracks(sp, lfm, variance=5, limit=12))