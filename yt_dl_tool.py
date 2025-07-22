from strands import tool
import yt_dlp
import os

def youtube_to_mp3(youtube_url: str, output_path: str) -> None:
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_path, 'audio.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
    except Exception as e:
        print(f"Error: {e}")

@tool(description="Download audio from a YouTube video and convert it to MP3 format. Takes a YouTube URL and optional output path.")
def download_youtube_audio(youtube_url: str, output_path: str = ".") -> str:
    """
    Download audio from a YouTube video and convert it to MP3 format.
    
    Args:
        youtube_url: The URL of the YouTube video to download
        output_path: The directory path where the audio file should be saved (default: current directory)
    
    Returns:
        A message indicating the success or failure of the download
    """
    try:
        print(f"Downloading audio from {youtube_url} to {output_path}")
        youtube_to_mp3(youtube_url, output_path)
        return f"Successfully downloaded audio from {youtube_url} to audio.mp3"
    except Exception as e:
        return f"Failed to download audio: {str(e)}"