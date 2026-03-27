---
name: video-learner
description: 分析视频内容，生成可调用的Skill。
---

# Video-Learner

## 触发条件

当用户发送抖音/B站/YouTube视频链接时，本Skill被调用。

## 环境要求

本Skill需要以下工具存在于环境中：
- `yt-dlp` - 视频下载
- `ffmpeg` - 音视频处理
- `whisper` - 语音识别（Python包）
- `node` + `douyin-download` - 抖音下载

如未安装，请先运行：
```bash
pip3 install yt-dlp openai-whisper
brew install ffmpeg node
npx clawhub install douyin-download
```

## 处理流程

1. 用 yt-dlp 或 douyin-download 下载视频
2. 用 ffmpeg 提取音频
3. 用 Whisper 本地转文字
4. 用自身LLM能力分析文字内容，提取：核心知识点、适用人群、难度
5. 展示分析结果给用户
6. 用户确认后，生成SKILL.md文件
7. 保存到 ~/.openclaw/workspace/skills/<自动命名>/SKILL.md

## 输出

- 内容摘要（3-5个核心知识点）
- 适用人群标签
- 难度等级（入门/进阶/高级）
- 生成的SKILL.md文件路径

## 限制

- 仅处理用户主动发送的视频链接
- 不主动获取其他内容
- 不存储视频文件（仅存文字和分析结果）
- 生成内容基于视频原始内容，不添加外部信息