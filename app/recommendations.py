"""
Recommends songs based on given songs.
"""

from pprint import pprint

from app.models import Track
from app.config import Settings
from app.spotify_client import SpotifyClient, get_top_tracks
from app.lastfm_client import LastfmClient

def recommend_tracks(
        spotify_client: SpotifyClient, 
        lastfm_client: LastfmClient,
        variance = 20, 
        offset = 0, 
        time_range = "medium_term",
        limit = 20
        ) -> list[Track]:
    """Get user's top tracks and recommend new ones.
    
    Args:
    - variance: Number of user's most listened to tracks 
        to base recommendations off of. Maxes out at 20.
    - limit: Number of recommended tracks to return. Maxes
        out at 200.
    ...
    """
    top_tracks = get_top_tracks(
        spotify_client, 
        limit=variance, 
        offset=offset,
        time_range=time_range,
    )

    recommended_tracks_array = []
    for track in top_tracks:
        similar_tracks = lastfm_client.get_similar_tracks(
            artist=track.artist,
            title=track.title
        )
        # Using a deque to easily grab from the front later
        if similar_tracks:
            recommended_tracks_array.append(similar_tracks)

    print("=========== TOP TRACKS: ===========")
    pprint(top_tracks)
    print("=========== RECOMMENDED TRACKS: ===========")
    pprint(recommended_tracks_array)

    result = []

    # Loop in column major
    for col in range(len(recommended_tracks_array[0])):
        for row in range(len(recommended_tracks_array)):
            # Grab top results in order for each song
            top_track = recommended_tracks_array[row][col]

            if top_track and top_track not in result:
                result.append(top_track)

            if limit == len(result):
                print("=========== RESULT: ===========")
                return result

    print("=========== RESULT: ===========")
    return result


if __name__ == '__main__':
    settings = Settings()
    sp = SpotifyClient(settings)
    lfm = LastfmClient(settings)
    pprint(recommend_tracks(sp, lfm, variance=4, limit=10))