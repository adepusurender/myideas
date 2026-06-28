import os
import sys
from pathlib import Path

# Add the current directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from video_to_subtitles import VideoToSubtitles

def main():
    # Example usage
    video_path = "example_video.mp4"
    output_path = "output_subtitles.srt"
    
    converter = VideoToSubtitles()
    converter.convert(video_path, output_path)
    print(f"Subtitles saved to {output_path}")

if __name__ == "__main__":
    main()
