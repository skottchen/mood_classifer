from moodify_api import get_random_songs 
from moodify_api import example_songs

def get_song_recommendations(song_name):
    # MOCKED return value for now
    return [
        get_random_songs("emotional", example_songs)
    ]