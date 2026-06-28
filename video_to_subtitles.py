import whisper
import re
import argparse
from docx import Document
from deep_translator import GoogleTranslator
import os
import sys
import time

def format_time(t):
    """
    Format time in seconds to SRT timestamp format: HH:MM:SS,mmm
    """
    hours = int(t // 3600)
    minutes = int((t % 3600) // 60)
    seconds = int(t % 60)
    millis = int((t - int(t)) * 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02},{millis:03}"

def clean_srt_content(content):
    """
    Clean SRT content by removing indices and timestamps.

    Args:
        content (str): Raw SRT content

    Returns:
        str: Cleaned text content
    """
    # Remove timestamps before subtitle indices so timestamp milliseconds are not
    # partially stripped by the index cleanup.
    cleaned = re.sub(r"^\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}\n?", "", content, flags=re.MULTILINE)
    # Remove subtitle indices
    cleaned = re.sub(r"^\d+\n", "", cleaned, flags=re.MULTILINE)
    # Clean up extra whitespace
    cleaned = re.sub(r"\n\s*\n", "\n", cleaned).strip()
    return cleaned

def save_as_docx(content, docx_file):
    """
    Save text content as a DOCX file.

    Args:
        content (str or list): Text content to save
        docx_file (str): Output DOCX file path
    """
    doc = Document()
    if isinstance(content, str):
        content = content.split("\n")

    for line in content:
        doc.add_paragraph(line)
    doc.save(docx_file)

def generate_srt(video_path, output_srt, model_size="small"):
    """
    Generate an SRT subtitle file from a video using Whisper with auto language detection.

    Args:
        video_path (str): Path to the video file
        output_srt (str): Output SRT file path
        model_size (str): Whisper model size

    Returns:
        tuple: (success: bool, detected_language: str or None)
    """
    try:
        model = whisper.load_model(model_size)
        result = model.transcribe(video_path, task="transcribe")
        detected_language = result.get("language", "unknown")

        with open(output_srt, "w", encoding="utf-8") as f:
            for i, segment in enumerate(result["segments"], start=1):
                start = segment["start"]
                end = segment["end"]
                text = segment["text"].strip()

                f.write(f"{i}\n")
                f.write(f"{format_time(start)} --> {format_time(end)}\n")
                f.write(f"{text}\n\n")

        print(f"🗣️ Detected language: {detected_language}")
        return True, detected_language
    except Exception as e:
        print(f"❌ Error generating subtitles: {e}")
        return False, None

def batch_translate(text_lines, source_lang, target_lang, batch_size=5):
    """
    Translate text lines in batches to reduce API calls (5-10x faster).
    
    Args:
        text_lines (list): List of text lines to translate
        source_lang (str): Source language code
        target_lang (str): Target language code
        batch_size (int): Number of lines to translate per batch
        
    Returns:
        list: Translated lines preserving original empty lines
    """
    translated_lines = []
    translator = GoogleTranslator(source=source_lang, target=target_lang)
    
    for i in range(0, len(text_lines), batch_size):
        batch = text_lines[i:i + batch_size]
        non_empty_lines = [line for line in batch if line.strip()]
        empty_indices = [j for j, line in enumerate(batch) if not line.strip()]
        
        if not non_empty_lines:
            translated_lines.extend(batch)
            continue
        
        try:
            # Join lines with a separator for batch translation
            batch_text = " |SEP| ".join(non_empty_lines)
            translated_batch = translator.translate(batch_text)
            
            # Split back into individual lines
            translated_batch_lines = translated_batch.split(" |SEP| ")
            
            # Rebuild with empty lines in original positions
            batch_result = []
            translated_idx = 0
            for j in range(len(batch)):
                if j in empty_indices:
                    batch_result.append("")
                else:
                    batch_result.append(translated_batch_lines[translated_idx] if translated_idx < len(translated_batch_lines) else "")
                    translated_idx += 1
            
            translated_lines.extend(batch_result)
            progress = min(i + batch_size, len(text_lines))
            print(f"  Translated {progress}/{len(text_lines)} lines...")
            
        except Exception as e:
            print(f"  ⚠️ Batch translation failed (lines {i}-{i+batch_size}): {e}")
            translated_lines.extend(batch)
    
    return translated_lines

def process_transcripts(srt_file, original_txt, original_docx, english_txt, english_docx, telugu_txt, telugu_docx, detected_language):
    """
    Process SRT file to generate original language, English, and Telugu transcripts with translation chain.
    Uses batch translation for 5-10x faster processing.

    Args:
        srt_file (str): Input SRT file path
        original_txt (str): Output original language TXT file path
        original_docx (str): Output original language DOCX file path
        english_txt (str): Output English TXT file path
        english_docx (str): Output English DOCX file path
        telugu_txt (str): Output Telugu TXT file path
        telugu_docx (str): Output Telugu DOCX file path
        detected_language (str): Language code detected by Whisper

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Read and clean SRT content
        with open(srt_file, "r", encoding="utf-8") as f:
            srt_content = f.read()

        original_text = clean_srt_content(srt_content)

        # Save original language files
        with open(original_txt, "w", encoding="utf-8") as f:
            f.write(original_text)

        save_as_docx(original_text, original_docx)
        print(f"✅ Original language ({detected_language}) transcript saved")

        # Translate to English if not already in English
        if detected_language.lower() == "en":
            english_text = original_text
            print("✅ Original language is English, skipping translation")
        else:
            print(f"🌍 Translating from {detected_language} to English (batched)...")
            text_lines = original_text.split("\n")
            english_lines = batch_translate(text_lines, detected_language, "en", batch_size=5)
            english_text = "\n".join(english_lines)

        # Save English files
        with open(english_txt, "w", encoding="utf-8") as f:
            f.write(english_text)

        save_as_docx(english_text, english_docx)
        print("✅ English transcript saved")

        # Translate to Telugu (batched)
        print("🌍 Translating to Telugu (batched)...")
        text_lines = english_text.split("\n")
        telugu_lines = batch_translate(text_lines, "en", "te", batch_size=5)

        # Save Telugu files
        with open(telugu_txt, "w", encoding="utf-8") as f:
            f.write("\n".join(telugu_lines))

        save_as_docx(telugu_lines, telugu_docx)
        print("✅ Telugu transcript saved")

        return True
    except Exception as e:
        print(f"❌ Error processing transcripts: {e}")
        return False

def process_video(mp4_file, model_size="small", skip_transcription=False):
    """
    Process a video file with auto language detection and generate transcripts with translation chain.
    Workflow: Auto-detect language → Original language transcript → Translate to English → Translate to Telugu

    Args:
        mp4_file (str): Path to the MP4 file
        model_size (str): Whisper model size
        skip_transcription (bool): If True, skip transcription and use existing SRT file

    Returns:
        bool: True if successful, False otherwise
    """
    if not os.path.exists(mp4_file):
        print(f"❌ Error: File '{mp4_file}' not found.")
        return False

    if not mp4_file.lower().endswith('.mp4'):
        print("❌ Error: Input must be an MP4 file.")
        return False

    # Get base name without extension
    base_name = os.path.splitext(mp4_file)[0]

    # Define output file names
    srt_file = f"{base_name}_subs.srt"
    original_txt = f"{base_name}_original.txt"
    original_docx = f"{base_name}_original.docx"
    english_txt = f"{base_name}.txt"
    english_docx = f"{base_name}.docx"
    telugu_txt = f"{base_name}_telugu.txt"
    telugu_docx = f"{base_name}_telugu.docx"

    start_time = time.time()
    detected_language = "unknown"

    # Check if SRT already exists and skip transcription if requested
    if skip_transcription and os.path.exists(srt_file):
        print(f"🎬 Using existing SRT: {srt_file}")
        # Try to detect language from existing original .txt if available
        if os.path.exists(original_txt):
            with open(original_txt, "r", encoding="utf-8") as f:
                sample = f.read(100)
                # Simple heuristic: check for Arabic characters
                if any('\u0600' <= c <= '\u06FF' for c in sample):
                    detected_language = "ar"
                elif any('\u0C00' <= c <= '\u0C7F' for c in sample):
                    detected_language = "te"
                else:
                    detected_language = "en"
        print(f"🗣️ Detected language (from existing): {detected_language}")
    else:
        print(f"🎬 Processing video: {mp4_file}")
        print("📝 Generating subtitles with language auto-detection...")

        # Step 1: Generate SRT from video
        success, detected_language = generate_srt(mp4_file, srt_file, model_size)
        if not success:
            return False

        srt_time = time.time()
        print(f"✅ SRT generated in {srt_time - start_time:.2f} seconds")

    print("📄 Processing transcripts with translation chain...")

    # Step 2 & 3: Process transcripts with translation chain
    if not process_transcripts(srt_file, original_txt, original_docx, english_txt, english_docx, telugu_txt, telugu_docx, detected_language):
        return False

    total_time = time.time() - start_time
    print(f"✅ Processing complete in {total_time:.2f} seconds")

    print("📁 Output files:")
    print(f"   📝 SRT: {srt_file}")
    print(f"   📄 Original ({detected_language}) TXT: {original_txt}")
    print(f"   📋 Original ({detected_language}) DOCX: {original_docx}")
    print(f"   📄 English TXT: {english_txt}")
    print(f"   📋 English DOCX: {english_docx}")
    print(f"   📄 Telugu TXT: {telugu_txt}")
    print(f"   📋 Telugu DOCX: {telugu_docx}")

    return True

def main():
    parser = argparse.ArgumentParser(
        description="Convert MP4 video to multilingual transcripts with auto language detection and translation chain",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Workflow: Auto-detect language → Original language transcript → English → Telugu

Examples:
  python video_to_subtitles.py video.mp4
  python video_to_subtitles.py video.mp4 --model medium
  python video_to_subtitles.py video.mp4 --skip-transcription
        """
    )

    parser.add_argument("mp4_file", help="Path to the MP4 video file")
    parser.add_argument(
        "--model",
        choices=["tiny", "base", "small", "medium", "large"],
        default="small",
        help="Whisper model size (default: small)"
    )
    parser.add_argument(
        "--skip-transcription",
        action="store_true",
        help="Skip SRT generation and use existing SRT file (faster for re-processing)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )

    args = parser.parse_args()

    if args.verbose:
        print(f"Using Whisper model: {args.model}")
        print(f"Skip transcription: {args.skip_transcription}")

    success = process_video(args.mp4_file, args.model, skip_transcription=args.skip_transcription)

    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
