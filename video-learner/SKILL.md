---
name: video-learner
description: 自动从视频（抖音/B站/YouTube）提取内容并生成OpenClaw Skill。包含：1.视频下载 2.语音识别转文字 3.LLM分析展示 4.用户确认后生成 5.自动安装到skills目录 6.可被调用使用。整个流程更安全、更可控。支持抖音无水印下载+B站/YouTube音频提取。
---

# Video-Learner - 视频学习工具

把视频变成可用的 Skill！

## 支持平台

- 🎵 **抖音** - 无水印视频下载 + 语音识别
- 📺 **B站** - 音频提取 + 语音识别  
- 🎬 **YouTube** - 音频提取 + 语音识别

## 功能

- **视频下载** - 支持抖音/B站/YouTube视频/音频提取
- **语音识别** - 用Whisper把音频转成文字（支持 tiny/small/base 模型）
- **LLM分析** - 先提取核心知识点、适用人群、难度等级
- **用户确认** - 分析结果展示给你，确认后再生成完整 Skill
- **自动安装** - 生成的 Skill 自动安装到 skills/ 目录
- **可调用** - 生成后可直接使用，我能在对话中调用

## 安全设计

1. **不直接记忆** - 不把知识点写进基础记忆，避免知识错乱
2. **来源标记** - 每个 Skill 标明来源视频
3. **确认机制** - 分析后需要用户确认才生成
4. **分开存储** - Skills 存单独目录，不影响基础能力

## 使用方法

### 1. 安装依赖

```bash
# 安装 yt-dlp（视频下载）
pip3 install yt-dlp

# 安装 Whisper（语音识别）
pip3 install openai-whisper

# 安装 ffmpeg（音视频处理）
brew install ffmpeg
```

### 2. 设置API Key

```bash
# 设置环境变量
export MINIMAX_API_KEY='你的API Key'
```

### 3. 使用方式

**通过对话使用（推荐）：**
- 直接发视频链接给我
- 我分析 → 展示 → 你确认 → 自动安装

**手动运行脚本：**
```bash
python3 ~/.openclaw/workspace/scripts/video-learner.py "视频链接" "Skill名称"
```

## 完整流程

```
1. 你发视频链接给我（抖音/B站/YouTube）
2. 我下载视频 + Whisper转文字
3. 我展示分析结果（核心知识点、适用人群、难度）
4. 你确认OK
5. 我生成完整Skill + 自动安装
6. 以后你可以直接使用这个Skill
```

## 注意事项

1. **API Key** - 需要自备MiniMax API Key，建议用环境变量设置
2. **抖音下载** - 需要 douyin-download skill 已安装
3. **B站限制** - 非会员只能下载低质量音频
4. **Whisper模型** - 首次运行下载模型(约500MB)，可以用 tiny/base/small
5. **隐私** - 生成的Skill不包含API Key，可以安全分享
6. **安全设计** - 不直接记忆知识点，避免知识错乱；需要确认才生成

## 示例

### 对话中使用

```bash
# 抖音视频
https://www.douyin.com/video/123456789

# B站视频
https://www.bilibili.com/video/BVxxx/

# YouTube视频
https://youtube.com/watch?v=xxx
```

生成 Skill 后，你可以这样用：
- 问"如何使用这个技能？"
- 问相关问题时我会调用这个 Skill 来回答

## 技术栈

- **下载**：yt-dlp + douyin-download
- **语音识别**：OpenAI Whisper
- **LLM分析**：MiniMax API
- **存储**：~/.openclaw/workspace/skills/