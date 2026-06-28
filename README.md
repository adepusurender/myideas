# Video to Multilingual Transcripts

Convert MP4 videos into multilingual transcripts with auto-language detection and translation chain: **Auto-detect → Original Language → English → Telugu**

Uses OpenAI's Whisper for speech-to-text transcription and Google Translate for multilingual translation.

---

## 🎯 Features

✅ **Auto Language Detection** - Automatically detects the language spoken in the video  
✅ **Multilingual Output** - Generates transcripts in original language, English, and Telugu  
✅ **Batch Translation** - 5-10x faster translation by batching API calls  
✅ **Multiple Formats** - Outputs both TXT and DOCX files  
✅ **GUI & CLI** - Desktop app and command-line interface  
✅ **Flexible Model Selection** - Choose Whisper model size (tiny to large)  
✅ **Fully Tested** - 31+ unit tests covering all functionality  

---

## 📋 Prerequisites

- **Python 3.8+**
- **FFmpeg** (required by Whisper for audio processing)

### Install FFmpeg

**Ubuntu/Debian:**
```bash
sudo apt-get install ffmpeg
```

**macOS (with Homebrew):**
```bash
brew install ffmpeg
```

**Windows:**
- Download from [ffmpeg.org](https://ffmpeg.org/download.html)
- Or use: `choco install ffmpeg`

---

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/adepusurender/myideas.git
cd myideas
```

### 2. Create Virtual Environment (Recommended)
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 💻 Usage

### Option 1: GUI Application (Easiest)

Launch the graphical interface:
```bash
python app.py
```

**Steps:**
1. Click "Select MP4 File" and choose your video
2. Select Whisper model size (default: small)
3. Click "Process Video"
4. Wait for completion message

### Option 2: Command Line

**Basic usage:**
```bash
python video_to_subtitles.py video.mp4
```

**With specific Whisper model:**
```bash
python video_to_subtitles.py video.mp4 --model medium
```

**Skip transcription (reuse existing SRT):**
```bash
python video_to_subtitles.py video.mp4 --skip-transcription
```

**Verbose output:**
```bash
python video_to_subtitles.py video.mp4 --model large -v
```

### Model Size Options

| Model | Size | Speed | Accuracy | VRAM | Notes |
|-------|------|-------|----------|------|-------|
| tiny | 39M | ⚡⚡⚡ | Low | 1GB | Fastest, lowest accuracy |
| base | 140M | ⚡⚡ | Medium | 1GB | Balanced |
| small | 466M | ⚡ | Good | 2GB | **Default** |
| medium | 1.5GB | Slow | High | 5GB | Very accurate |
| large | 2.9GB | ⚠️ Slow | ⚠️ Best | 10GB | Highest accuracy |

---

## 📁 Output Files

For each input video `video.mp4`, the following files are generated in the same directory:

```
video_subs.srt              # SRT subtitle file with timestamps
video_original.txt          # Original language transcript (TXT)
video_original.docx         # Original language transcript (DOCX)
video.txt                   # English translation (TXT)
video.docx                  # English translation (DOCX)
video_telugu.txt            # Telugu translation (TXT)
video_telugu.docx           # Telugu translation (DOCX)
```

---

## 🧪 Testing

Run the comprehensive test suite to validate the source code:

### Using Test Runner
```bash
python run_tests.py
```

### Using Unittest
```bash
python -m unittest discover -s . -p "test_*.py" -v
```

### Using Pytest
```bash
pip install pytest pytest-cov
pytest test_video_to_subtitles.py -v --cov=.
```

**Test Coverage:** 31 test cases covering:
- ✅ Time formatting for SRT
- ✅ SRT content cleaning
- ✅ DOCX file generation
- ✅ Batch translation
- ✅ Language detection
- ✅ Transcript processing
- ✅ Video processing workflow
- ✅ Error handling and edge cases

---

## 📊 Source Code Structure

### `video_to_subtitles.py`
Main module with all processing functions:

| Function | Purpose |
|----------|---------|
| `format_time()` | Convert seconds to SRT timestamp format |
| `clean_srt_content()` | Remove indices and timestamps from SRT |
| `save_as_docx()` | Save text content as DOCX file |
| `generate_srt()` | Transcribe video using Whisper |
| `batch_translate()` | Translate text in batches (5-10x faster) |
| `process_transcripts()` | Generate multilingual transcripts |
| `process_video()` | Main orchestration function |

### `app.py`
Tkinter-based GUI application with:
- File selection dialog
- Model size dropdown
- Process button with status updates
- Success/error notifications

### `test_video_to_subtitles.py`
Comprehensive unit tests with 31 test cases:
- Mocked Whisper and Google Translator
- Temporary file handling
- Edge case coverage
- Error scenario testing

### `run_tests.py`
Test runner script for easy test execution

---

## 🔄 Workflow

```
MP4 Video
    ↓
[Whisper] → Auto-detect language
    ↓
Generate SRT with timestamps
    ↓
Extract original language transcript
    ↓
[Translate to English]
    ↓
[Translate to Telugu]
    ↓
Output Files (SRT, TXT, DOCX for each language)
```

---

## ⚙️ Advanced Usage

### Custom Python Script
```python
from video_to_subtitles import process_video

# Process video with custom settings
result = process_video(
    mp4_file="path/to/video.mp4",
    model_size="medium",
    skip_transcription=False
)

if result:
    print("✅ Processing complete!")
else:
    print("❌ Processing failed!")
```

### Batch Processing
```python
import os
from video_to_subtitles import process_video

video_dir = "path/to/videos"
for video_file in os.listdir(video_dir):
    if video_file.endswith(".mp4"):
        print(f"Processing {video_file}...")
        process_video(os.path.join(video_dir, video_file), model_size="small")
```

---

## 🐛 Troubleshooting

### "FFmpeg not found"
**Solution:** Install FFmpeg using the commands in Prerequisites section

### "CUDA out of memory"
**Solution:** Use a smaller model size (tiny or base)

### "Translation failed"
**Solution:** Check internet connection (Google Translate API requires internet)

### "Whisper model download slow"
**Solution:** Pre-download model: `python -c "import whisper; whisper.load_model('small')"`

---

## 📦 Dependencies

```
openai-whisper==20231117    # Speech-to-text transcription
deep-translator==1.11.4     # Translation service
python-docx==0.8.11         # DOCX file generation
pytest==7.4.0               # Testing framework (optional)
pytest-cov==4.1.0           # Code coverage (optional)
```

---

## 📄 License

This project is part of the "My Ideas" repository.

---

## 🤝 Contributing

Found a bug or want to improve this? Feel free to:
1. Report issues
2. Submit pull requests
3. Suggest new features

---

## 📞 Support

For issues, questions, or suggestions:
- Check the test suite in `test_video_to_subtitles.py`
- Review the source code documentation in `video_to_subtitles.py`
- Run tests: `python run_tests.py`

---

## 🎓 Examples

### Example 1: Process English Video
```bash
python video_to_subtitles.py lecture.mp4 --model small
```
**Output:** English SRT + original transcripts + Telugu translation

### Example 2: Process Spanish Video
```bash
python video_to_subtitles.py entrevista.mp4 --model medium
```
**Output:** Spanish SRT + original transcripts + English translation + Telugu translation

### Example 3: High Accuracy Processing
```bash
python video_to_subtitles.py conference.mp4 --model large
```
**Output:** High-quality transcription with all translations

---

**Created:** 2026-06-28  
**Latest Update:** 2026-06-28  
**Repository:** [adepusurender/myideas](https://github.com/adepusurender/myideas)
