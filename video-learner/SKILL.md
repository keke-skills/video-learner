---
name: video-learner
description: 分析视频内容，生成可调用的Skill。
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

## 声明

本Skill需要以下工具和访问权限：
- **工具**：python3, yt-dlp, ffmpeg, whisper (Python包), node
- **依赖Skill**：douyin-download（需要node运行）
- **写入路径**：~/.openclaw/workspace/skills/

## 触发条件

当用户发送抖音/B站/YouTube视频链接时，本Skill被调用。

## 处理流程

1. 在 `/tmp/` 创建临时目录下载视频
2. 用 yt-dlp 或 douyin-download 下载视频
3. 用 ffmpeg 提取音频
4. 用 Whisper 本地转文字
5. 用本Agent的LLM能力分析文字内容
6. 展示分析结果给用户
7. 用户确认后，在 ~/.openclaw/workspace/skills/<新Skill名>/ 生成SKILL.md
8. 处理完成后删除临时视频文件

## 安全说明

- Whisper：本地运行，不发送音频到外部
- 内容分析：使用本Agent的模型能力
- 临时文件：处理后自动清理
- 用户确认：生成新Skill需要用户明确确认
- 生成的Skill存在 ~/.openclaw/workspace/skills/，可随时删除

## 限制

- 仅处理用户主动发送的视频链接
- 不主动获取其他内容
- 不存储视频文件