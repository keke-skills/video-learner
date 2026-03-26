# Video-Learner(BiliBili/Douyin/Youtube)

把视频变成可用的 OpenClaw Skill！

## 更新日志
- 🗓 **2026年3月26日**

## 功能

- 📥 **视频下载** - 支持抖音/B站/YouTube
- 🎙️ **语音识别** - 用 Whisper 转文字
- ✅ **用户确认** - 分析后确认再生成
- 📦 **自动安装** - 安装到 skills 目录
- 🔄 **可调用** - 对话中直接使用

## 支持平台

| 平台 | 状态 |
|------|------|
| 🎵 抖音 | ✅ |
| 📺 B站 | ✅ |
| 🎬 YouTube | ✅ |

## 使用方式（推荐）

**直接发视频链接给 OpenClaw：**
- 发抖音/B站/YouTube 链接给我
- 我自动处理：下载 → 识别 → 分析 → 确认 → 生成 → 安装
- 不需要额外配置任何东西

## 手动运行（可选）

如果想自己跑脚本：

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

### 3. 运行

```bash
python3 video-learner.py "视频链接" "Skill名称"
```

## 安全设计

- ✅ 不需要额外 LLM 配置（使用 OpenClaw 本身的能力）
- ✅ 需要用户确认才生成
- ✅ 不直接记忆知识点（避免知识错乱）
- ✅ 分开存储，不影响基础能力

## 文件结构

```
video-learner/
├── video-learner.py      # 主脚本（可选）
├── video-learner/        # Skill 目录
│   └── SKILL.md         # Skill 说明
└── README.md            # 本文件
```

## License

MIT
