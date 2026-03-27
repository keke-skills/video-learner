---
name: video-learner
description: Analyze video content and generate a callable OpenClaw Skill.
requires:
  binaries:
    - python3
    - yt-dlp
    - ffmpeg
    - whisper
    - node
  skills:
    - douyin-download
  paths:
    - ~/.openclaw/workspace/skills/
---

# Video-Learner

## Overview

Convert any video (Douyin/BiliBili/YouTube) into a callable OpenClaw Skill.

## Declared Requirements

- **Tools**: python3, yt-dlp, ffmpeg, whisper (Python), node
- **Dependency**: douyin-download (requires node)
- **Write access**: ~/.openclaw/workspace/skills/

## Trigger

When the user sends a Douyin/BiliBili/YouTube video link, this skill is invoked.

## Processing Flow

1. Create temp directory in `/tmp/` for video download
2. Download video using yt-dlp or douyin-download
3. Extract audio using ffmpeg
4. Transcribe audio to text using Whisper (local)
5. Analyze text content using the agent's LLM capability
6. Display analysis results to user
7. After user confirmation, generate SKILL.md to ~/.openclaw/workspace/skills/<new-skill-name>/
8. Delete temp video files after processing

## Security Notes

- Whisper: Runs locally, no audio sent to external services
- Content analysis: Uses the agent's own model capability
- Temp files: Automatically cleaned up after processing
- User confirmation: Required before generating new Skill
- Generated Skills are stored in ~/.openclaw/workspace/skills/ and can be deleted anytime

## Limitations

- Only processes user-provided video links
- Does not proactively fetch other content
- Does not store video files