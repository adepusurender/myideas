import os
import subprocess
import json
from typing import Optional, List, Dict
from pathlib import Path

class VideoToSubtitles:
    """
    A class to convert video files to subtitles using various methods.
    Supports OpenAI Whisper API and local models.
    """
    
    def __init__(self, model: str = "base", language: Optional[str] = None):
        """
        Initialize the VideoToSubtitles converter.
        
        Args:
            model: Model size (tiny, base, small, medium, large)
            language: Language code (e.g., 'en', 'es'). If None, auto-detect.
        """
        self.model = model
        self.language = language
        self.audio_temp = "temp_audio.wav"
    
    def extract_audio(self, video_path: str) -> str:
        """
        Extract audio from video file.
        
        Args:
            video_path: Path to the video file
            
        Returns:
            Path to the extracted audio file
        """
        try:
            cmd = [
                "ffmpeg",
                "-i", video_path,
                "-q:a", "9",
                "-n",
                self.audio_temp
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            return self.audio_temp
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to extract audio: {e}")
    
    def transcribe_audio(self, audio_path: str) -> str:
        """
        Transcribe audio to text using Whisper.
        
        Args:
            audio_path: Path to the audio file
            
        Returns:
            Transcribed text
        """
        try:
            cmd = ["whisper", audio_path, "--model", self.model, "--output_format", "vtt"]
            if self.language:
                cmd.extend(["--language", self.language])
            
            subprocess.run(cmd, check=True)
            return audio_path.replace(".wav", ".vtt")
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to transcribe audio: {e}")
    
    def convert_vtt_to_srt(self, vtt_path: str, srt_path: str) -> None:
        """
        Convert VTT subtitle format to SRT format.
        
        Args:
            vtt_path: Path to the VTT file
            srt_path: Path to save the SRT file
        """
        with open(vtt_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        srt_lines = []
        counter = 1
        
        for line in lines:
            if line.startswith('WEBVTT'):
                continue
            elif line.startswith('NOTE'):
                continue
            elif '-->' in line:
                # Convert timestamp format from VTT to SRT
                time_parts = line.split(' --> ')
                start = time_parts[0].replace('.', ',')
                end = time_parts[1].rstrip().replace('.', ',')
                srt_lines.append(str(counter) + '\n')
                srt_lines.append(f"{start} --> {end}\n")
                counter += 1
            elif line.strip():
                srt_lines.append(line)
            else:
                if srt_lines and srt_lines[-1] != '\n':
                    srt_lines.append('\n')
        
        with open(srt_path, 'w', encoding='utf-8') as f:
            f.writelines(srt_lines)
    
    def convert(self, video_path: str, output_path: str = None) -> str:
        """
        Convert video to subtitles in SRT format.
        
        Args:
            video_path: Path to the video file
            output_path: Path to save the subtitles (optional)
            
        Returns:
            Path to the generated subtitle file
        """
        if not output_path:
            base_name = Path(video_path).stem
            output_path = f"{base_name}_subtitles.srt"
        
        try:
            # Extract audio
            audio_path = self.extract_audio(video_path)
            
            # Transcribe audio
            vtt_path = self.transcribe_audio(audio_path)
            
            # Convert to SRT
            self.convert_vtt_to_srt(vtt_path, output_path)
            
            # Cleanup
            if os.path.exists(self.audio_temp):
                os.remove(self.audio_temp)
            if os.path.exists(vtt_path):
                os.remove(vtt_path)
            
            return output_path
        except Exception as e:
            raise Exception(f"Conversion failed: {e}")
