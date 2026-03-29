---
description: Extract video frames at specific timestamps from transcripts using ffmpeg — see what was on screen when something was said
user-invocable: true
---

# Extract Frames from Video

Extract video frames to see exactly what was on screen at a given moment. Use transcript timestamps to seek to the right position, then capture screenshots with ffmpeg.

## When to Use

- A transcript mentions something ambiguous — extract the frame to see what the user was looking at
- You need visual evidence (e.g., for a bug report or ticket)
- You want to correlate what was said with what was shown on screen

## Step 1: Find the Timestamp

Use whichever transcript format is available:

### JSON transcript (Whisper output)
```bash
python3 -c "
import json
with open('transcripts/video.json') as f:
    data = json.load(f)
for seg in data['segments']:
    if 'search phrase' in seg['text'].lower():
        print(f\"{seg['start']:.0f}s = {int(seg['start'])//60}m{int(seg['start'])%60}s: {seg['text']}\")
"
```

### SRT transcript
```bash
grep -B1 'search phrase' transcripts/video.srt
```

### Plain text (no timestamps)
Estimate position proportionally:
```bash
python3 -c "
import subprocess, json
text = open('transcripts/video.txt').read()
pos = text.lower().find('search phrase')
# Get video duration
probe = subprocess.run(['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', 'video.mp4'], capture_output=True, text=True)
duration = float(json.loads(probe.stdout)['format']['duration'])
est = int((pos / len(text)) * duration)
print(f'Estimated: {est//60}m{est%60}s ({est}s)')
"
```

## Step 2: Extract Frames

Extract a spread of frames around the timestamp to account for estimation error:

```bash
mkdir -p frames
VIDEO="path/to/video.mp4"

for ts in 15m00s 15m20s 15m40s 16m00s 16m20s; do
  secs=$(echo "$ts" | sed 's/m/*60+/;s/s//' | bc)
  ffmpeg -y -ss "$secs" -i "$VIDEO" -frames:v 1 -q:v 2 "frames/${ts}.jpg" 2>/dev/null
done
```

Key flags:
- `-ss` before `-i` — fast seeking (avoids decoding from start)
- `-frames:v 1` — extract exactly one frame
- `-q:v 2` — high-quality JPEG (lower = better, range 2–31)

## Step 3: Review Frames

Open or read each extracted frame to find the one showing the relevant UI state. Look for:
- URL bar (which app or page)
- Form fields, dropdowns, tables
- Error messages or unexpected states
- What the user was hovering or clicking

## Prerequisites

- `ffmpeg` installed and on PATH
- A transcript (produced by the `transcribe` skill or any other source)
