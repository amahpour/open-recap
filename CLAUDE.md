# open-recap

Video transcription and frame extraction toolkit. Transcribe what was said, see what was on screen.

## Structure

- `src/open_recap/` — Python package
  - `cli.py` — CLI entry point (argparse)
  - `transcriber.py` — core transcription logic (Whisper)
- `.claude/skills/` — Claude Code skill files
  - `transcribe.md` — transcribe videos
  - `extract-frames.md` — extract frames at timestamps
- `tests/` — test suite

## Commands

```bash
# Install (editable)
pip install -e .

# Run
open-recap /path/to/video.mp4

# Run with specific model
open-recap /path/to/videos/ --model medium
```

## Dependencies

- Python 3.9+
- `openai-whisper` (pip)
- `ffmpeg` (system)
