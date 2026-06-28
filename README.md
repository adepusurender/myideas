# My Ideas

Utilities for converting MP4 videos into transcripts using Whisper, then translating the transcript to English and Telugu.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Whisper also requires `ffmpeg` to be installed on your system.

## Command Line Usage

```bash
python video_to_subtitles.py path/to/video.mp4
```

Optional model size:

```bash
python video_to_subtitles.py path/to/video.mp4 --model medium
```

Reuse an existing generated SRT:

```bash
python video_to_subtitles.py path/to/video.mp4 --skip-transcription
```

## GUI Usage

```bash
python app.py
```

Generated transcript files are written next to the input video and are ignored by Git by default.
