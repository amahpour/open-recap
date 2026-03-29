"""Core transcription logic using OpenAI Whisper."""

import os
import glob

import whisper
from whisper.utils import get_writer

VIDEO_EXTENSIONS = (".mp4", ".mov")
WHISPER_MODELS = ["tiny", "base", "small", "medium", "large", "turbo"]
OUTPUT_FORMATS = ["txt", "vtt", "srt", "tsv", "json"]


def find_video_files(directory="."):
    """Find all MP4 and MOV files in the specified directory (case-insensitive)."""
    video_patterns = ["*.mp4", "*.MP4", "*.mov", "*.MOV"]
    video_files = []

    for pattern in video_patterns:
        video_files.extend(glob.glob(os.path.join(directory, pattern)))

    # Deduplicate while preserving order
    seen = set()
    unique = []
    for f in video_files:
        if f not in seen:
            seen.add(f)
            unique.append(f)

    return sorted(unique)


def transcribe_video(model, video_path, output_dir="transcripts"):
    """Transcribe a single video file and save all output formats.

    Returns the output directory path on success, None on failure.
    """
    print(f"Transcribing: {video_path}")
    os.makedirs(output_dir, exist_ok=True)

    try:
        result = model.transcribe(video_path, language="english", fp16=False)

        for fmt in OUTPUT_FORMATS:
            writer = get_writer(fmt, output_dir)
            writer(result, video_path)

        print(f"  Transcripts saved to: {output_dir}")
        return output_dir

    except Exception as e:
        print(f"  Error transcribing {video_path}: {e}")
        return None
