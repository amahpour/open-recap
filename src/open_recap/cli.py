"""CLI entry point for open-recap."""

import os
import time
import argparse
from pathlib import Path

import whisper

from .transcriber import (
    VIDEO_EXTENSIONS,
    WHISPER_MODELS,
    find_video_files,
    transcribe_video,
)


def main():
    """Transcribe video files — single file or entire directory."""
    parser = argparse.ArgumentParser(
        description="Transcribe videos using OpenAI Whisper. "
        "Pass a directory to transcribe all MP4/MOV files, or a single video file."
    )
    parser.add_argument(
        "path",
        type=str,
        help="Path to a video file (.mp4, .mov) or a directory containing videos",
    )
    parser.add_argument(
        "--model",
        "-m",
        type=str,
        default="turbo",
        choices=WHISPER_MODELS,
        help="Whisper model to use (default: turbo)",
    )
    args = parser.parse_args()

    # Normalize path (handle trailing slashes, quotes)
    raw_path = args.path.strip("\"'").rstrip("\\/")
    input_path = os.path.normpath(raw_path)

    if not os.path.isabs(input_path):
        input_path = os.path.abspath(input_path)

    # Determine file vs directory
    if os.path.isfile(input_path):
        if Path(input_path).suffix.lower() not in VIDEO_EXTENSIONS:
            print(
                f"Error: Not a supported video file. "
                f"Expected .mp4 or .mov, got: {Path(input_path).suffix}"
            )
            return
        video_files = [input_path]
        base_dir = os.path.dirname(input_path)
    elif os.path.isdir(input_path):
        base_dir = input_path
        video_files = find_video_files(input_path)
        if not video_files:
            print(f"No MP4 or MOV files found in: {input_path}")
            return
    else:
        print(f"Error: Path does not exist: {input_path}")
        return

    print("open-recap — Video Transcription")
    print("=" * 50)
    print(f"Input: {input_path}")
    print(f"Videos to transcribe: {len(video_files)}")
    print()
    for i, f in enumerate(video_files, 1):
        print(f"  {i}. {f}")
    print()

    # Load model
    print(f"Loading Whisper '{args.model}' model...")
    try:
        model = whisper.load_model(args.model)
        print("Model loaded successfully.")
    except Exception as e:
        print(f"Error loading model: {e}")
        return

    print()

    output_dir = os.path.join(base_dir, "transcripts")
    successful = 0
    failed = 0
    total_start = time.time()

    for i, video_file in enumerate(video_files, 1):
        print(f"[{i}/{len(video_files)}] Processing: {os.path.basename(video_file)}")

        start = time.time()
        result = transcribe_video(model, video_file, output_dir)
        elapsed = time.time() - start

        if result:
            successful += 1
            print(f"  Completed in {elapsed:.1f}s")
        else:
            failed += 1
        print()

    # Summary
    total_elapsed = time.time() - total_start
    minutes, seconds = divmod(int(total_elapsed), 60)
    print("=" * 50)
    print("SUMMARY")
    print("=" * 50)
    print(f"Total files: {len(video_files)}")
    print(f"Successful:  {successful}")
    print(f"Failed:      {failed}")
    print(f"Total time:  {minutes}m {seconds}s")
    if successful > 0:
        print(f"\nTranscripts saved in: {output_dir}")


if __name__ == "__main__":
    main()
