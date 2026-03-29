# open-recap

Transcribe videos and extract visual context from recordings. A homebrewed transcribe what was said, then see what was on screen.

Built on [OpenAI Whisper](https://github.com/openai/whisper) for transcription and `ffmpeg` for frame extraction.

## Features

- **Transcribe** MP4/MOV files to text, SRT, VTT, TSV, and JSON
- **Extract frames** at specific timestamps to see what was on screen
- **Claude Code skills** included — use `/transcribe` and `/extract-frames` as slash commands

## Install

```bash
pip install -e .
```

Requires `ffmpeg` on your PATH:
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# Windows
winget install ffmpeg
```

## Usage

### Transcribe a video
```bash
open-recap /path/to/video.mp4
```

### Transcribe all videos in a directory
```bash
open-recap /path/to/videos/
```

### Choose a Whisper model
```bash
open-recap /path/to/video.mp4 --model medium
```

Available models: `tiny`, `base`, `small`, `medium`, `large`, `turbo` (default).

### Extract a frame at a timestamp
```bash
ffmpeg -y -ss 120 -i video.mp4 -frames:v 1 -q:v 2 frame-2m00s.jpg
```

See the [extract-frames skill](.claude/skills/extract-frames.md) for the full workflow: find timestamps in transcripts, extract frames, review what was on screen.

## Output

Transcripts are saved to a `transcripts/` subfolder next to the input:

```
transcripts/
├── video.txt       # plain text
├── video.srt       # SubRip subtitles
├── video.vtt       # WebVTT subtitles
├── video.tsv       # tab-separated
└── video.json      # full Whisper output with segments
```

## Claude Code Skills

This repo includes two [Claude Code skills](https://docs.anthropic.com/en/docs/claude-code/skills):

| Skill | Description |
|-------|-------------|
| `/transcribe` | Transcribe video files to multiple formats |
| `/extract-frames` | Extract video frames at transcript timestamps |

To use them, open this repo in Claude Code — the skills are automatically available.

## License

[MIT](LICENSE) — Ari Mahpour
