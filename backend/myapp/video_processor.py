import ffmpeg
import os
import time
import assemblyai as aai
from faster_whisper import WhisperModel
from myapp.chat import translate

os.environ["IMAGEIO_FFMPEG_EXE"] = "/opt/homebrew/bin/ffmpeg"

# Assembly AI API Key
aai.settings.api_key = "0313003043464cee84fc5cd0e9bd7c9d"

# Configurations
AUDIO_FOLDER = 'audios'
TRANSCRIPT_FOLDER = 'transcripts'
SUBTITLE_FOLDER = 'subtitles'
OUTPUT_FOLDER = 'output'

# Ensure the extracted audio folder exists
os.makedirs(AUDIO_FOLDER, exist_ok=True)
os.makedirs(TRANSCRIPT_FOLDER, exist_ok=True)
os.makedirs(SUBTITLE_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def extract_audio(filepath, filename):
    audio_name = filename.split(".")[0] # Select the name of the video without extension
    extracted_audio = f"audio-{audio_name}.wav"
    audio_path = os.path.join(AUDIO_FOLDER, extracted_audio)
    stream = ffmpeg.input(filepath)
    stream = ffmpeg.output(stream, audio_path, bitrate="16k")
    ffmpeg.run(stream, overwrite_output=True)
    return extracted_audio, audio_path


def transcribe_using_whisper(audio):
    model = WhisperModel("small")
    segments, info = model.transcribe(audio, language="en")
    language = info[0]
    segments = list(segments)
    for segment in segments:
        print("[%.2fs -> %.2fs] %s" %
              (segment.start, segment.end, segment.text))
    return language, segments


def transcribe_using_assemblyai(audio_path, audio_name, lang=None, target_language=None):
    transcriber = aai.Transcriber()
    input_audio_name = audio_name.split(".")[0]
    srt_file_name = f"subtitle-{input_audio_name}.srt"
    transcript_file_name = f"transcript-{input_audio_name}.txt"
    srt_path = os.path.join(SUBTITLE_FOLDER, srt_file_name)
    transcript_path = os.path.join(TRANSCRIPT_FOLDER, transcript_file_name)
        
    if lang:
        # if we know the dominant language
        config = aai.TranscriptionConfig(speaker_labels=True, language_code=lang)
    else:
        config = aai.TranscriptionConfig(speaker_labels=True, language_detection=True)

    transcript = transcriber.transcribe(audio_path, config)

    if transcript.error:
        return None

    srt = transcript.export_subtitles_srt()
    with open(srt_path, "w") as srt_file:
        srt_file.write(srt)

    with open(transcript_path, 'w') as transcript_file:
        sentences = transcript.get_sentences()
        for sentence in sentences:
            transcript_file.write(sentence.text + "\n\n")
            
    if target_language:
        translate(transcript_path, target_language)
        translate(srt_path, target_language)

    return srt_path, transcript_path


def add_subtitle_to_video(soft_subtitle, subtitle_file,  subtitle_language, video_path, video_name):
    output_video_name = video_name.split(".")[0]
    video_input_stream = ffmpeg.input(video_path)
    subtitle_input_stream = ffmpeg.input(subtitle_file)
    output_video = f"output-{output_video_name}.mp4"
    output_video_path = os.path.join(OUTPUT_FOLDER, output_video)
    
    subtitle_track_title = subtitle_file.replace(".srt", "")

    if soft_subtitle:
        stream = ffmpeg.output(
            video_input_stream, subtitle_input_stream, output_video_path, **{"c": "copy", "c:s": "mov_text"},
            **{"metadata:s:s:0": f"language={subtitle_language}",
            "metadata:s:s:0": f"title={subtitle_track_title}"}
        )
        ffmpeg.run(stream, overwrite_output=True)
    else:
        stream = ffmpeg.output(video_input_stream, output_video_path,

                               vf=f"subtitles={subtitle_file}")

        ffmpeg.run(stream, overwrite_output=True)

    return output_video_path
