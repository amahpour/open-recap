---
description: Transcribe video files (MP4/MOV) to text, subtitles, and structured JSON using OpenAI Whisper
user-invocable: true
---

# Transcribe Video

Transcribe video files using OpenAI Whisper. Produces transcripts in multiple formats: plain text, SRT, VTT, TSV, and JSON.

## Usage

The user will provide a path to a video file or a directory containing videos.

### Single file
```bash
open-recap /path/to/video.mp4
```

### Entire directory
```bash
open-recap /path/to/videos/
```

### Choose a model
```bash
open-recap /path/to/video.mp4 --model medium
```

Available models (smallest → largest): `tiny`, `base`, `small`, `medium`, `large`, `turbo` (default).

## Output

Transcripts are saved to a `transcripts/` subfolder next to the input file(s). Each video produces five files:
- `*.txt` — plain text
- `*.srt` — SubRip subtitles (with timestamps)
- `*.vtt` — WebVTT subtitles
- `*.tsv` — tab-separated (start, end, text)
- `*.json` — full Whisper output with segments, timestamps, and confidence

## Prerequisites

- Python 3.9+
- `ffmpeg` installed and on PATH
- Install the package: `pip install -e .` (from the repo root)
