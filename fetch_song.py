# import lyricsgenius
# genius = lyricsgenius.Genius("-sweRw7rUyLIfYikh0EJE9BMEApiyBIi3WcV8t8JzYhrGc4gEwl3fMKFibCdeRHk")
# def fetch_lyrics(title, artist):
#     """
#     Fetch lyrics from Genius for a given song.
#     """
#     song = genius.search_song(title, artist)
#     if song:
#         lyrics = song.lyrics.split("\n")
#         return [{"time": i * 3000, "text": line} for i, line in enumerate(lyrics)]
#     return []

# if __name__ == '__main__':
#     print(fetch_lyrics('Thôi Em Đừng Đi','RPT MCK')) #for testing only
import requests

def fetch_lyrics(title, artist):
    """
    Fetch time-synchronized lyrics from Textyl API.
    :param title: Song title.
    :param artist: Artist name.
    :return: List of dictionaries with 'time' (ms) and 'text' (lyric line).
    """
    query = f"{artist} {title}"
    url = f"https://api.textyl.co/api/lyrics?q={query}"
    try:
        response = requests.get(url, verify=False)  # Disable SSL verification
        response.raise_for_status()
        data = response.json()
        return process_textyl_output(data)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching lyrics: {e}")
        return []

def process_textyl_output(data):
    """
    Process the Textyl API output into app-friendly format.
    :param data: List of dictionaries with 'seconds' and 'lyrics'.
    :return: List of dictionaries with 'time' in ms and 'text'.
    """
    processed_lyrics = []
    for entry in data: # loop through each dictionaty in the list and append into processed_lyrics list
        processed_lyrics.append({
            "time": entry["seconds"] * 1000 - 300,  # Convert seconds to milliseconds 1000 is to convert to mx, 300 is the offset for pragram delay
            "text": entry["lyrics"]
        })
    return processed_lyrics


if __name__ == "__main__":
    lyrics = fetch_lyrics("APT.", "ROSÉ")
    for line in lyrics:
        print(f"{line['time']}ms: {line['text']}")
