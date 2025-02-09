import yt_dlp
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from youtubesearchpython import VideosSearch
from dotenv import load_dotenv

load_dotenv()
def setup_spotify():
    client_id = os.getenv('client_id')
    client_secret = os.getenv('client_secret')

    

    client_credentials_manager = SpotifyClientCredentials(
        client_id=client_id, 
        client_secret=client_secret
    )
    return spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_spotify_tracks(sp, url):
    # Extract playlist ID from URL
    playlist_id = url.split('/')[-1].split('?')[0]
    
    tracks = []
    results = sp.playlist_tracks(playlist_id)
    
    for item in results['items']:
        track = item['track']
        track_name = track['name']
        artists = [artist['name'] for artist in track['artists']]
        search_query = f"{track_name} {' '.join(artists)}"
        
        # Find YouTube URL
        videos_search = VideosSearch(search_query, limit=1)
        results = videos_search.result()
        
        if results and results['result']:
            youtube_url = f"https://youtube.com/watch?v={results['result'][0]['id']}"
            tracks.append({
                'name': f"{track_name} - {', '.join(artists)}",
                'url': youtube_url
            })
    
    return tracks

def download_playlist_audio(url, is_spotify=False):
    if not os.path.exists('songs'):
        os.makedirs('songs')

    def progress_hook(d):
        if d['status'] == 'downloading' and d.get('_percent_str') == '  0.0%':
            print(f"Started downloading: {d['filename']}")
        elif d['status'] == 'finished':
            print(f"Finished downloading: {d['filename']}")

    ydl_opts = {
        'format': 'bestaudio[abr<=128]/bestaudio',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': 'songs/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '128'
        }],
        'progress_hooks': [progress_hook],
        'ignoreerrors': True,
        'concurrent_fragment_downloads': 30,
        'buffersize': 8192,
        'format_sort': ['abr:128'],
        'postprocessor_args': ['-q:a', '0'],
        'lazy_playlist': True,
        'n_threads': 4,
    }

    try:
        if is_spotify:
            sp = setup_spotify()
            tracks = get_spotify_tracks(sp, url)
            print(f"Found {len(tracks)} tracks in Spotify playlist")
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                for track in tracks:
                    print(f"\nProcessing: {track['name']}")
                    ydl.download([track['url']])
        else:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                error_code = ydl.download([url])
                if error_code != 0:
                    print("Some videos were skipped due to unavailability")
                    return False
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False
    return True

def download_playlist_video(url):
    def progress_hook(d):
        if d['status'] == 'downloading' and d.get('_percent_str') == '  0.0%':
            print(f"Started downloading: {d['filename']}")

        elif d['status'] == 'finished':
            print(f"Finished downloading: {d['filename']}")

    if not os.path.exists('videos'):
        os.makedirs('videos')

    ydl_opts = {
        'format': 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]/best',
        'outtmpl': 'videos/%(title)s.%(ext)s',
        'progress_hooks': [progress_hook],
        'ignoreerrors': True,
        'concurrent_fragment_downloads': 30,
        'buffersize': 4096,
        'lazy_playlist': True,
        'n_threads': 4,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            error_code = ydl.download([url])
            if error_code != 0:
                print("Some videos were skipped due to unavailability")
                return False
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False
    return True

if __name__ == "__main__":
    url = input("Enter the YouTube or Spotify playlist URL: ")
    if not url.strip():
        print("Please enter a valid URL")
        success = False
    else:
        mode = input("Download as audio (a) or video (v)? ").lower()
        if mode == 'a':
            is_spotify = 'spotify.com' in url.lower()
            success = download_playlist_audio(url, is_spotify)
        elif mode == 'v':
            if 'spotify.com' in url.lower():
                print("Video download not available for Spotify URLs")
                success = False
            else:
                success = download_playlist_video(url)
        else:
            print("Invalid mode selected")
            success = False
            
        if success:
            print("Download completed successfully")
