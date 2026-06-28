# Video to Subtitles

A Python utility to automatically convert video files to subtitle files using OpenAI's Whisper model for speech-to-text transcription.

## Overview

This project extracts audio from video files and converts it to subtitle files (SRT format) using the Whisper speech recognition model. It's useful for:

- Creating subtitles for videos in multiple languages
- Automatic transcription of video content
- Accessibility enhancement for videos
- Batch processing of video files

## Features

- 🎬 Extract audio from video files
- 🎯 Transcribe audio to text using OpenAI Whisper
- 📝 Convert transcriptions to SRT subtitle format
- 🌍 Multi-language support with auto-detection
- 🔄 Flexible model selection (tiny, base, small, medium, large)
- 🧹 Automatic cleanup of temporary files

## Requirements

- Python 3.7+
- FFmpeg (for audio extraction)
- OpenAI Whisper
- ffmpeg-python (optional, for programmatic use)

## Installation

### 1. Install FFmpeg

**On macOS:**
```bash
brew install ffmpeg
```

**On Ubuntu/Debian:**
```bash
sudo apt-get install ffmpeg
```

**On Windows:**
Download from https://ffmpeg.org/download.html or use:
```bash
choco install ffmpeg
```

### 2. Install Python Dependencies

```bash
pip install openai-whisper
```

## Usage

### Basic Usage

```python
from video_to_subtitles import VideoToSubtitles

# Create converter instance
converter = VideoToSubtitles(model="base")

# Convert video to subtitles
subtitle_path = converter.convert("path/to/video.mp4")
print(f"Subtitles saved to: {subtitle_path}")
```

### Advanced Usage

```python
# Specify output path and language
converter = VideoToSubtitles(model="base", language="en")
subtitle_path = converter.convert(
    video_path="path/to/video.mp4",
    output_path="custom_subtitles.srt"
)
```

### Model Options

- `tiny` - Fastest, lowest accuracy (~39MB)
- `base` - Good balance (141MB) - **Recommended**
- `small` - Better accuracy (461MB)
- `medium` - High accuracy (1.5GB)
- `large` - Best accuracy (2.9GB)

## Class Methods

### `__init__(model: str = "base", language: Optional[str] = None)`
Initialize the converter with specified model and language.

### `extract_audio(video_path: str) -> str`
Extract audio from video file and save as WAV.

### `transcribe_audio(audio_path: str) -> str`
Transcribe audio to text using Whisper model.

### `convert_vtt_to_srt(vtt_path: str, srt_path: str) -> None`
Convert VTT subtitle format to SRT format.

### `convert(video_path: str, output_path: str = None) -> str`
Main method to convert video to subtitles (SRT format).

## Output Format

The tool outputs SRT (SubRip) format subtitles:

```
1
00:00:00,000 --> 00:00:05,000
This is the first subtitle.

2
00:00:05,000 --> 00:00:10,000
This is the second subtitle.
```

## Supported Video Formats

Any format supported by FFmpeg:
- MP4, AVI, MOV, MKV, WMV, FLV, WebM, etc.

## Performance Tips

- Use smaller models (`tiny`, `base`) for faster processing
- Use larger models for better accuracy with difficult audio
- Process multiple videos in parallel using threading/multiprocessing
- Consider GPU acceleration if available (CUDA-enabled GPU)

## Error Handling

The tool raises exceptions with descriptive messages:

```python
try:
    converter.convert("video.mp4")
except Exception as e:
    print(f"Error: {e}")
```

Common issues:
- FFmpeg not installed: Install FFmpeg first
- Whisper not installed: `pip install openai-whisper`
- Invalid video format: Check file format and try a different one

## License

This project is open for personal use and experimentation.

---

*Part of the myideas collection for day-to-day projects*
