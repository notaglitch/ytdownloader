import yt_dlp

def download_playlist(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': 'ytdl/%(title)s.%(ext)s',  # Added ytdl/ directory prefix
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }]
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
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
