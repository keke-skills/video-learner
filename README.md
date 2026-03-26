# Video-Learner 🎥

把视频变成可用的 OpenClaw Skill！

## ⚠️ 重要提醒

**使用前必须先安装依赖！** 否则无法正常工作。

```bash
# 安装 yt-dlp（视频下载）
pip3 install yt-dlp

# 安装 Whisper（语音识别）
pip3 install openai-whisper

# 安装 ffmpeg（音视频处理）
brew install ffmpeg

# 安装 Node.js（抖音下载需要）
brew install node
```

## 功能

- 📥 **视频下载** - 支持抖音/B站/YouTube（已内置抖音下载）
- 🎙️ **语音识别** - 用 Whisper 转文字
- ✅ **用户确认** - 分析后确认再生成
- 📦 **自动安装** - 安装到 skills 目录
- 🔄 **可调用** - 对话中直接使用

## 支持平台

| 平台 | 状态 |
|------|------|
| 🎵 抖音 | ✅ 已内置下载器 |
| 📺 B站 | ✅ |
| 🎬 YouTube | ✅ |

## 使用方式（推荐）

**直接发视频链接给 OpenClaw：**
- 发抖音/B站/YouTube 链接给我
- 我自动处理：下载 → 识别 → 分析 → 确认 → 生成 → 安装
- 不需要额外配置任何东西

## 手动运行（可选）

### 1. 克隆仓库

```bash
git clone https://github.com/wd-skills/video-learner.git
cd video-learner
```

### 2. 安装依赖（必须！）

```bash
# 安装 yt-dlp
pip3 install yt-dlp

# 安装 Whisper
pip3 install openai-whisper

# 安装 ffmpeg
brew install ffmpeg

# 安装 Node.js
brew install node
```

### 3. 运行

```bash
python3 video-learner.py "视频链接" "Skill名称"
```

## 文件结构

```
video-learner/
├── video-learner.py      # 主脚本
├── douyin-download/      # 内置抖音下载器（已整合）
│   └── douyin.js
├── video-learner/        # Skill 目录
│   └── SKILL.md
└── README.md
```

## License

MIT