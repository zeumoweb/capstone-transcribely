import os
import uuid
import ffmpeg
from pydub import AudioSegment
from moviepy.editor import VideoFileClip, AudioFileClip
from google.cloud import translate_v2 as translate
from google.cloud import texttospeech
import assemblyai as aai

import whisper
import spacy
from spacy_syllables import SpacySyllables
from tqdm import tqdm
import tempfile
import re

os.environ['path'] = '/opt/homebrew/bin/ffmpeg'

os.environ["IMAGEIO_FFMPEG_EXE"] = "/opt/homebrew/bin/ffmpeg"

# Assembly AI API Key
aai.settings.api_key = # Add Key

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


spacy_models = {
    "english": "en_core_web_sm",
    "german": "de_core_news_sm",
    "french": "fr_core_news_sm",
    "italian": "it_core_news_sm",
    "catalan": "ca_core_news_sm",
    "chinese": "zh_core_web_sm",
    "croatian": "hr_core_news_sm",
    "danish": "da_core_news_sm",
    "dutch": "nl_core_news_sm",
    "finnish": "fi_core_news_sm",
    "greek": "el_core_news_sm",
    "japanese": "ja_core_news_sm",
    "korean": "ko_core_news_sm",
    "lithuanian": "lt_core_news_sm",
    "macedonian": "mk_core_news_sm",
    "polish": "pl_core_news_sm",
    "portuguese": "pt_core_news_sm",
    "romanian": "ro_core_news_sm",
    "russian": "ru_core_news_sm",
    "spanish": "es_core_news_sm",
    "swedish": "sv_core_news_sm",
    "ukrainian": "uk_core_news_sm"
}

def extract_audio_from_video(filename):
    audio_name = filename.split(".")[0] # Select the name of the video without extension
    audio_name = audio_name.split("/")[-1]
    extracted_audio = f"audio-{audio_name}.wav"
    stream = ffmpeg.input(filename)
    stream = ffmpeg.output(stream, extracted_audio, bitrate="16k")
    ffmpeg.run(stream, overwrite_output=True)
    return extracted_audio


def transcribe_audio(audio_file, source_language):
    try:
        model = whisper.load_model("tiny")
        trans = model.transcribe(audio_file, language=source_language, verbose=False, word_timestamps=True)
        return trans
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return None


def translate_text(texts, target_language):
    try:
        translate_client = translate.Client()
        results = translate_client.translate(texts, target_language=target_language)
        return [result['translatedText'] for result in results]
    except Exception as e:
        print(f"Error translating texts: {e}")
        return None


def create_audio_from_text(text, target_language, target_voice):
    audio_file =  os.path.join(AUDIO_FOLDER, "translated_" + str(uuid.uuid4()) + ".wav")
    try:
        client = texttospeech.TextToSpeechClient()
        input_text = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code=target_language,
            name=target_voice
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16, speaking_rate=1
        )
        response = client.synthesize_speech(
            request={"input": input_text, "voice": voice, "audio_config": audio_config}
        )
        with open(audio_file, "wb") as out:
            out.write(response.audio_content)
        return audio_file
    except Exception as e:
        if os.path.isfile(audio_file):
            os.remove(audio_file)
        raise Exception(f"Error creating audio from text: {e}")


ABBREVIATIONS = {
    "Mr.": "Mister",
    "Mrs.": "Misses",
    "No.": "Number",
    "Dr.": "Doctor",
    "Ms.": "Miss",
    "Ave.": "Avenue",
    "Blvd.": "Boulevard",
    "Ln.": "Lane",
    "Rd.": "Road",
    "a.m.": "before noon",
    "p.m.": "after noon",
    "ft.": "feet",
    "hr.": "hour",
    "min.": "minute",
    "sq.": "square",
    "St.": "street",
    "Asst.": "assistant",
    "Corp.": "corporation"
}

ISWORD = re.compile(r'.*\w.*')


# Constants
DUCKING_GAIN = -10
FADE_DURATION = 500
CHUNK_SIZE = 128

def merge_audio_files(transcription, source_language, target_language, target_voice, audio_file):
    temp_files = []
    try:
        ducked_audio = load_audio(audio_file)
        nlp = load_spacy_model(source_language)
        sentences, sentence_starts, sentence_ends = extract_sentences(transcription, nlp)

        translated_texts = translate_sentences(sentences, target_language)
        merged_audio = create_translated_audio_track(
            ducked_audio, translated_texts, sentence_starts, sentence_ends, target_language, target_voice, temp_files
        )

        return merged_audio, ducked_audio

    except Exception as e:
        print(f"Error merging audio files: {e}")
        return None

    finally:
        cleanup_temp_files(temp_files)

def load_audio(audio_file):
    return AudioSegment.from_wav(audio_file)

def load_spacy_model(language):
    spacy_model = spacy_models[language]
    if spacy_model not in spacy.util.get_installed_models():
        spacy.cli.download(spacy_model)
    nlp = spacy.load(spacy_model)
    nlp.add_pipe("syllables", after="tagger")
    return nlp

def extract_sentences(transcription, nlp):
    sentences = []
    sentence_starts = []
    sentence_ends = []
    sentence = ""
    sent_start = 0

    for segment in tqdm(transcription["segments"]):
        if segment["text"].isupper():
            continue

        for i, word in enumerate(segment["words"]):
            if not ISWORD.search(word["word"]):
                continue

            word["word"] = ABBREVIATIONS.get(word["word"].strip(), word["word"])
            sentence, sent_start = update_sentence(sentence, word, segment, nlp, i, sent_start)

            if word["word"].endswith("."):
                sentences.append(sentence)
                sentence_starts.append(sent_start)
                sentence_ends.append(word["end"])
                sentence, sent_start = "", 0

    return sentences, sentence_starts, sentence_ends

def update_sentence(sentence, word, segment, nlp, index, sent_start):
    sentence += adjust_word_format(word["word"], sentence)

    if index == 0 or sent_start == 0:
        word_speed = calculate_word_speed(word, nlp)
        sent_start = determine_sentence_start_time(word, segment, word_speed, nlp)

    if index == len(segment["words"]) - 1:
        word_speed = calculate_word_speed(word, nlp)
        segment_speed = calculate_segment_speed(segment, nlp)
        if should_add_period(word_speed, segment_speed):
            word["word"] += "."

    return sentence, sent_start

def adjust_word_format(word, sentence):
    if word.startswith("-"):
        return sentence[:-1] + word + " "
    return word + " "

def calculate_word_speed(word, nlp):
    word_syllables = sum(token._.syllables_count for token in nlp(word["word"]) if token._.syllables_count)
    return word_syllables / (word["end"] - word["start"])

def calculate_segment_speed(segment, nlp):
    segment_syllables = sum(token._.syllables_count for token in nlp(segment["text"]) if token._.syllables_count)
    return segment_syllables / (segment["end"] - segment["start"])

def determine_sentence_start_time(word, segment, word_speed, nlp):
    if word_speed < 3:
        return word["end"] - sum(token._.syllables_count for token in nlp(word["word"]) if token._.syllables_count) / 3
    return word["start"]

def should_add_period(word_speed, segment_speed):
    return word_speed < 1.0 or segment_speed < 2.0

def translate_sentences(sentences, target_language):
    translated_texts = []
    print("Translating sentences")

    for i in tqdm(range(0, len(sentences), CHUNK_SIZE)):
        chunk = sentences[i:i + CHUNK_SIZE]
        translated_chunk = translate_text(chunk, target_language)
        if translated_chunk is None:
            raise Exception("Translation failed")
        translated_texts.extend(translated_chunk)

    return translated_texts

def create_translated_audio_track(ducked_audio, translated_texts, sentence_starts, sentence_ends, target_language, target_voice, temp_files):
    merged_audio = AudioSegment.silent(duration=0)
    prev_end_time = 0

    print("Creating translated audio track")
    for i, translated_text in enumerate(tqdm(translated_texts)):
        translated_audio, temp_file = create_translated_audio(translated_text, target_language, target_voice, temp_files)

        ducked_audio = apply_ducking_effect(ducked_audio, translated_audio, sentence_starts[i], prev_end_time, len(translated_texts), i, sentence_ends[i])
        merged_audio = merge_audio_segments(merged_audio, translated_audio, sentence_ends[i], prev_end_time)
        prev_end_time = sentence_starts[i] * 1000

    return merged_audio

def create_translated_audio(translated_text, target_language, target_voice, temp_files):
    translated_audio_file = create_audio_from_text(translated_text, target_language, target_voice)
    if translated_audio_file is None:
        raise Exception("Audio creation failed")
    temp_files.append(translated_audio_file)
    translated_audio = AudioSegment.from_wav(translated_audio_file)
    return translated_audio, translated_audio_file

def apply_ducking_effect(ducked_audio, translated_audio, start_time, prev_end_time, total_texts, index, sentence_end):
    start_time_ms = int(start_time * 1000)
    end_time_ms = start_time_ms + len(translated_audio)
    next_start_time_ms = int(sentence_start * 1000) if index < total_texts - 1 else len(ducked_audio)

    ducked_segment = ducked_audio[start_time_ms:end_time_ms].apply_gain(DUCKING_GAIN)
    fade_out_duration = min(FADE_DURATION, max(1, start_time_ms - prev_end_time))
    fade_in_duration = min(FADE_DURATION, max(1, next_start_time_ms - end_time_ms))

    if start_time_ms == 0:
        ducked_audio = ducked_segment + ducked_audio[end_time_ms:].fade_in(fade_in_duration)
    elif end_time_ms == len(ducked_audio):
        ducked_audio = ducked_audio[:start_time_ms].fade_out(fade_out_duration) + ducked_segment
    else:
        ducked_audio = ducked_audio[:start_time_ms].fade_out(fade_out_duration) + ducked_segment + ducked_audio[end_time_ms:].fade_in(fade_in_duration)

    return ducked_audio.overlay(translated_audio, position=start_time_ms)

def merge_audio_segments(merged_audio, translated_audio, sentence_end, prev_end_time):
    original_duration = int(sentence_end * 1000)
    new_duration = len(translated_audio) + len(merged_audio)
    padding_duration = max(0, original_duration - new_duration)
    padding = AudioSegment.silent(duration=padding_duration)
    return merged_audio + padding + translated_audio

def cleanup_temp_files(temp_files):
    for file in temp_files:
        try:
            os.remove(file)
        except Exception as e:
            print(f"Error removing temporary file {file}: {e}")



def save_audio_to_file(audio, filename):
    try:
        audio.export(filename, format="wav")
        print(f"Audio track with translation only saved to {filename}")
    except Exception as e:
        print(f"Error saving audio to file: {e}")



def add_audio_in_video(video_file, new_audio):
    try:
        # Load the video
        video = VideoFileClip(video_file)

        # Save the new audio to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
            new_audio.export(temp_audio_file.name, format="wav")
        new_audio.export("duckled.wav", format="wav")

        # Load the new audio into an AudioFileClip
        try:
            new_audio_clip = AudioFileClip(temp_audio_file.name)
        except Exception as e:
            print(f"Error loading new audio into an AudioFileClip: {e}")
            return

        # Check if the audio is compatible with the video
        if new_audio_clip.duration < video.duration:
            print("Warning: The new audio is shorter than the video. The remaining video will have no sound.")
        elif new_audio_clip.duration > video.duration:
            print("Warning: The new audio is longer than the video. The extra audio will be cut off.")
            new_audio_clip = new_audio_clip.subclip(0, video.duration)

        # Set the audio of the video to the new audio
        video = video.set_audio(new_audio_clip)

        # Write the result to a new video file
        output_filename = os.path.splitext(video_file)[0] + "_translated.mp4"
        try:
            video.write_videofile(output_filename, audio_codec='aac')
        except Exception as e:
            print(f"Error writing the new video file: {e}")
            return

        print(f"Translated video saved as {output_filename}")

    except Exception as e:
        print(f"Error replacing audio in video: {e}")
    finally:
        # Remove the temporary audio file
        if os.path.isfile(temp_audio_file.name):
            os.remove(temp_audio_file.name)
        
        return output_filename

def generate_dub(input, voice, credentials, source_language):
    # Set the GOOGLE_APPLICATION_CREDENTIALS environment variable
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials

    audio_file = extract_audio_from_video(input)
    if audio_file is None:
        return

    transcription = transcribe_audio(audio_file, source_language.lower())
    if transcription is None:
        return

    merged_audio, ducked_audio = merge_audio_files(transcription, source_language.lower(), voice[:5], voice, audio_file)
    if merged_audio is None:
        return
    output_video_path = add_audio_in_video(input, ducked_audio)
    # Save the audio file with the same name as the video file but with a ".wav" extension
    video_name = input.split("/")[-1]
    output_filename = os.path.join(AUDIO_FOLDER, video_name + ".wav")
    save_audio_to_file(merged_audio, output_filename)
    
    return output_video_path