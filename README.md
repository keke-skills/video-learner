# Video-Learner 🎥

把视频变成可用的 OpenClaw Skill！

## 功能

- 📥 **视频下载** - 支持抖音/B站/YouTube
- 🎙️ **语音识别** - 用 Whisper 转文字
- 🤖 **多LLM支持** - 支持 MiniMax/OpenAI/Claude
- ✅ **用户确认** - 分析后确认再生成
- 📦 **自动安装** - 安装到 skills 目录
- 🔄 **可调用** - 对话中直接使用

## 支持平台

| 平台 | 状态 |
|------|------|
| 🎵 抖音 | ✅ |
| 📺 B站 | ✅ |
| 🎬 YouTube | ✅ |

## 支持的 LLM

| 提供商 | 环境变量 | 默认模型 |
|--------|----------|----------|
| MiniMax | `MINIMAX_API_KEY` | MiniMax-M2.5 |
| OpenAI | `OPENAI_API_KEY` | gpt-4o-mini |
| Claude | `CLAUDE_API_KEY` | claude-3-haiku |

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/wd-skills/video-learner.git
cd video-learner
```

### 2. 安装依赖

```bash
# 安装 yt-dlp
pip3 install yt-dlp

# 安装 Whisper
pip3 install openai-whisper

# 安装 ffmpeg
brew install ffmpeg
```

### 3. 配置 LLM

```bash
# 选择 LLM 提供商
export LLM_PROVIDER=minimax  # 或 openai, claude

# 设置 API Key
export MINIMAX_API_KEY='你的API Key'
# 或
export OPENAI_API_KEY='你的API Key'
# 或
export CLAUDE_API_KEY='你的API Key'
```

### 4. 使用

```bash
python3 video-learner.py "视频链接" "Skill名称"

# 示例
python3 video-learner.py "https://www.bilibili.com/video/BVxxx/" "我的技能"
```

## 通过对话使用（推荐）

直接发视频链接给我，我自动处理：
- 下载 → 识别 → 分析 → 确认 → 生成 → 安装

## 安全设计

- ✅ API Key 不包含在代码中（使用环境变量）
- ✅ 需要用户确认才生成
- ✅ 不直接记忆知识点（避免知识错乱）
- ✅ 分开存储，不影响基础能力

## 文件结构

```
video-learner/
├── video-learner.py      # 主脚本
├── video-learner/        # Skill 目录
│   └── SKILL.md         # Skill 说明
└── README.md            # 本文件
```

## License

MIT