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
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])


@tool(description="Download audio from a YouTube video and convert it to MP3. Takes a YouTube URL and optional output path, returns a success message with the saved file path.")
def download_youtube_audio(youtube_url: str, output_path: str = ".") -> str:
    """
    Download audio from a YouTube video and save it as an MP3 file.

    Use this tool when you need to extract the audio track from a YouTube video
    for transcription, analysis, or sharing. Provide the YouTube video URL and
    an optional output directory. The resulting file is saved as `audio.mp3` in
    the specified directory; if a file with the same name already exists, it
    will be overwritten.

    This tool uses `yt-dlp` with FFmpeg to download the best available audio and
    transcode it to MP3 at approximately 192 kbps.

    Example response:
        "Successfully downloaded audio from https://youtu.be/abc123 to ./audio.mp3"

    Notes:
        - Requires FFmpeg to be installed and available on your PATH
        - Only the audio track is saved; no video is downloaded
        - Output filename is fixed to `audio.mp3` in `output_path`
        - Network restrictions, age-restricted/private videos, or region locks
          may prevent downloads
        - Status messages are printed to stdout; on success, this function
          returns a success message including the saved file path; on errors, it
          returns an error string starting with "Failed to download audio:"

    Args:
        youtube_url: The URL of the YouTube video to download. Example:
                     "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        output_path: The directory where the audio file should be saved
                     (default: current directory "."). The directory must exist.

    Returns:
        On success: A success message (string) containing the saved file path,
                    e.g., "Successfully downloaded audio from <URL> to ./audio.mp3"
        On failure: An error message (string) starting with
                    "Failed to download audio: ..."
    """
    try:
        print(f"Downloading audio from {youtube_url} to {output_path}")
        youtube_to_mp3(youtube_url, output_path)
        return f"Successfully downloaded audio from {youtube_url} to {output_path}/audio.mp3"
    except Exception as e:
        return f"Failed to download audio: {str(e)}"