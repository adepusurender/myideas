import unittest
import tempfile
import os
from pathlib import Path
from video_to_subtitles import VideoToSubtitles

class TestVideoToSubtitles(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures."""
        self.converter = VideoToSubtitles(model="base")
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test files."""
        for file in os.listdir(self.temp_dir):
            file_path = os.path.join(self.temp_dir, file)
            if os.path.isfile(file_path):
                os.unlink(file_path)
        os.rmdir(self.temp_dir)
    
    def test_initialization(self):
        """Test VideoToSubtitles initialization."""
        self.assertEqual(self.converter.model, "base")
        self.assertIsNone(self.converter.language)
    
    def test_initialization_with_language(self):
        """Test VideoToSubtitles initialization with language."""
        converter = VideoToSubtitles(model="small", language="es")
        self.assertEqual(converter.model, "small")
        self.assertEqual(converter.language, "es")
    
    def test_convert_vtt_to_srt(self):
        """Test VTT to SRT conversion."""
        # Create a temporary VTT file
        vtt_content = """WEBVTT

00:00:01.000 --> 00:00:05.000
Hello, this is a test.

00:00:06.000 --> 00:00:10.000
This is the second subtitle.
"""
        vtt_path = os.path.join(self.temp_dir, "test.vtt")
        srt_path = os.path.join(self.temp_dir, "test.srt")
        
        with open(vtt_path, 'w', encoding='utf-8') as f:
            f.write(vtt_content)
        
        # Convert
        self.converter.convert_vtt_to_srt(vtt_path, srt_path)
        
        # Verify
        self.assertTrue(os.path.exists(srt_path))
        with open(srt_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        self.assertIn('1', content)
        self.assertIn('00:00:01,000 --> 00:00:05,000', content)
        self.assertIn('Hello, this is a test.', content)
    
    def test_convert_vtt_to_srt_with_multiple_subtitles(self):
        """Test VTT to SRT conversion with multiple subtitles."""
        vtt_content = """WEBVTT

NOTE This is a comment

00:00:01.000 --> 00:00:05.000
First subtitle

00:00:06.000 --> 00:00:10.000
Second subtitle

00:00:11.000 --> 00:00:15.000
Third subtitle
"""
        vtt_path = os.path.join(self.temp_dir, "test_multi.vtt")
        srt_path = os.path.join(self.temp_dir, "test_multi.srt")
        
        with open(vtt_path, 'w', encoding='utf-8') as f:
            f.write(vtt_content)
        
        self.converter.convert_vtt_to_srt(vtt_path, srt_path)
        
        with open(srt_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check all subtitles are present
        self.assertIn('1', content)
        self.assertIn('2', content)
        self.assertIn('3', content)
        self.assertIn('First subtitle', content)
        self.assertIn('Second subtitle', content)
        self.assertIn('Third subtitle', content)
    
    def test_vtt_to_srt_empty_file(self):
        """Test VTT to SRT conversion with empty file."""
        vtt_content = "WEBVTT\n\n"
        vtt_path = os.path.join(self.temp_dir, "empty.vtt")
        srt_path = os.path.join(self.temp_dir, "empty.srt")
        
        with open(vtt_path, 'w', encoding='utf-8') as f:
            f.write(vtt_content)
        
        self.converter.convert_vtt_to_srt(vtt_path, srt_path)
        self.assertTrue(os.path.exists(srt_path))
    
    def test_model_sizes(self):
        """Test different model sizes."""
        models = ["tiny", "base", "small", "medium", "large"]
        for model in models:
            converter = VideoToSubtitles(model=model)
            self.assertEqual(converter.model, model)
    
    def test_multiple_languages(self):
        """Test initialization with different languages."""
        languages = ["en", "es", "fr", "de", "it"]
        for lang in languages:
            converter = VideoToSubtitles(language=lang)
            self.assertEqual(converter.language, lang)

if __name__ == '__main__':
    unittest.main()
