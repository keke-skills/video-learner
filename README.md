# Video-Learner 🎥

把视频变成可用的 OpenClaw Skill！

## 功能

- 📥 **视频下载** - 支持抖音/B站/YouTube
- 🎙️ **语音识别** - 用 Whisper 转文字
- 🤖 **LLM分析** - 提取核心知识点
- ✅ **用户确认** - 分析后确认再生成
- 📦 **自动安装** - 安装到 skills 目录
- 🔄 **可调用** - 对话中直接使用

## 支持平台

| 平台 | 状态 |
|------|------|
| 🎵 抖音 | ✅ |
| 📺 B站 | ✅ |
| 🎬 YouTube | ✅ |

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/wd-skills/my-skill.git
cd my-skill
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

### 3. 设置 API Key

```bash
export MINIMAX_API_KEY='你的API Key'
```

### 4. 使用

**通过对话（推荐）：**
- 发视频链接给我
- 我自动处理

**手动运行：**
```bash
python3 video-learner.py "视频链接" "Skill名称"
```

## 流程

```
发视频 → 下载+识别 → 分析展示 → 确认 → 生成+安装 → 可调用
```

## 安全设计

- ✅ 不直接记忆知识点（避免知识错乱）
- ✅ 需要用户确认才生成
- ✅ API Key 不包含在代码中
- ✅ 分开存储，不影响基础能力

## 文件结构

```
my-skill/
├── video-learner.py      # 主脚本
├── video-learner/       # Skill 目录
│   └── SKILL.md        # Skill 说明
└── README.md           # 本文件
```

## License

MIT