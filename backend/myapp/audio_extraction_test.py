import unittest
from unittest.mock import patch, call, MagicMock
import os
from video_processor import extract_audio

AUDIO_FOLDER = "audios"

class TestExtractAudio(unittest.TestCase):
    @patch("ffmpeg.run")
    @patch("ffmpeg.output")
    @patch("ffmpeg.input")
    @patch("os.path.join")
    def test_extract_audio_success(self, mock_path_join, mock_ffmpeg_input, mock_ffmpeg_output, mock_ffmpeg_run):
        filepath = "/mock/file.mp4"
        filename = "file.mp4"
        expected_audio_name = "audio-file.mp3"
        expected_audio_path = "audios/audio-file.mp3"
        
        mock_path_join.return_value = expected_audio_path
        mock_ffmpeg_input.return_value = "mock_stream_input"
        mock_ffmpeg_output.return_value = "mock_stream_output"
        mock_ffmpeg_run.return_value = None  # ffmpeg.run() has no return value

        extracted_audio, audio_path = extract_audio(filepath, filename)
        self.assertEqual(extracted_audio, expected_audio_name)
        self.assertEqual(audio_path, expected_audio_path)

        mock_ffmpeg_input.assert_called_once_with(filepath)
        mock_ffmpeg_output.assert_called_once_with("mock_stream_input", expected_audio_path, bitrate="16k")
        mock_ffmpeg_run.assert_called_once_with("mock_stream_output", overwrite_output=True)
        mock_path_join.assert_called_once_with(AUDIO_FOLDER, expected_audio_name)


    @patch("ffmpeg.run")
    @patch("ffmpeg.output")
    @patch("ffmpeg.input")
    @patch("os.path.join")
    def test_extract_audio_invalid_filename(self, mock_path_join, mock_ffmpeg_input, mock_ffmpeg_output, mock_ffmpeg_run):
        filepath = "file.mp4"
        filename = "file"  # No extension
        expected_audio_name = "audio-file.mp3"
        expected_audio_path = "audios/audio-file.mp3"
        
        mock_path_join.return_value = expected_audio_path
        mock_ffmpeg_input.return_value = "mock_stream_input"
        mock_ffmpeg_output.return_value = "mock_stream_output"
        mock_ffmpeg_run.return_value = None  # ffmpeg.run() has no return value

        extracted_audio, audio_path = extract_audio(filepath, filename)
        
        self.assertEqual(extracted_audio, expected_audio_name)
        self.assertEqual(audio_path, expected_audio_path)

        mock_ffmpeg_input.assert_called_once_with(filepath)
        mock_ffmpeg_output.assert_called_once_with("mock_stream_input", expected_audio_path, bitrate="16k")
        mock_ffmpeg_run.assert_called_once_with("mock_stream_output", overwrite_output=True)
        mock_path_join.assert_called_once_with(AUDIO_FOLDER, expected_audio_name)

if __name__ == "__main__":
    unittest.main()
