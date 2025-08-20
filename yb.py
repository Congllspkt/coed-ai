import yt_dlp

def download_youtube_video_1080p_mp4(url, output_path='D:/'):
    """
    Downloads a YouTube video in 1080p MP4 format.

    Args:
        url (str): The URL of the YouTube video.
        output_path (str): The directory where the video will be saved.
                           Defaults to the current directory.
    """
    ydl_opts = {
        'format': 'bestvideo[height<=1080]+bestaudio/best',
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"Video downloaded successfully to {output_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


v = "3GZa9x9vioQ"
video_url = "https://www.youtube.com/watch?v=" + v
download_youtube_video_1080p_mp4(video_url)