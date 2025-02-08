import yt_dlp

def download_playlist(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': 'songs/%(title)s.%(ext)s',  # Added ytdl/ directory prefix
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }],
        'progress_hooks': [lambda d: print(f"Downloading: {d['filename']} - {d['_percent_str']} complete")], # Add progress hook
        'ignoreerrors': True  # Skip unavailable videos
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
    url = input("Enter the playlist URL: ")
    if not url.strip():  # Check for empty input
        print("Please enter a valid URL")
    else:
        success = download_playlist(url)
        if success:
            print("Download completed successfully")
