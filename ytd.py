import yt_dlp
import os

def download_playlist_audio(url):
    def progress_hook(d):
        if d['status'] == 'downloading' and d.get('_percent_str') == '  0.0%':
            print(f"Started downloading: {d['filename']}")

        elif d['status'] == 'finished':
            print(f"Finished downloading: {d['filename']}")

    if not os.path.exists('songs'):
        os.makedirs('songs')

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
        'buffersize': 4096,
        'format_sort': ['abr:128'],
        'postprocessor_args': ['-q:a', '0'],
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
    url = input("Enter the youtube video/playlist URL: ")
    if not url.strip():
        print("Please enter a valid URL")
        success = False
    else:
        mode = input("Download as audio (a) or video (v)? ").lower()
        if mode == 'a':
            success = download_playlist_audio(url)
        elif mode == 'v':
            success = download_playlist_video(url)
        else:
            print("Invalid mode selected")
            success = False
            
        if success:
            print("Download completed successfully")
