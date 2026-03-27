---
name: video-learner
description: Analyze video content and generate a callable OpenClaw Skill.
---

# Video-Learner

## Overview

Convert any video (Douyin/BiliBili/YouTube) into a callable OpenClaw Skill.

## How It Works

1. User sends a video link
2. This agent downloads, transcribes, and analyzes the video
3. Analysis results are shown to user
4. After user confirmation, a new SKILL.md is created in ~/.openclaw/workspace/skills/
5. New skills are created in **disabled** state and require manual enable

## Required Tools

This skill uses these tools at runtime:
- **yt-dlp** - Download videos
- **ffmpeg** - Extract audio
- **whisper** - Transcribe audio to text (local, no network upload)
- **node** + **douyin-download** - For Douyin videos
- **python3** - Required by whisper

If tools are missing, the agent will report which ones need installation.

## Key Points

- **User confirmation required**: Agent cannot generate skills without explicit approval
- **Generated skills are disabled**: New skills are saved but not auto-enabled
- **Manual review**: User must manually inspect and enable any generated skill
- **Temp files cleaned**: Downloaded videos are deleted after processing
- **Local transcription**: Audio is transcribed locally, not sent to external services

## Trigger

When the user sends a Douyin/BiliBili/YouTube video link, this skill is invoked.

## Security Notes

- Whisper runs locally - no audio sent to external services
- Content analysis uses the agent's own model capability
- User confirmation required before generating any skill
- Generated skills are disabled until user enables them
- Can delete any generated skill from ~/.openclaw/workspace/skills/ anytime

## Limitations

- Only processes user-provided video links
- Does not proactively fetch other content
- Does not store video files
- Cannot auto-enable generated skills