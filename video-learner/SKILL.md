---
name: video-learner
description: 自动从视频（抖音/B站/YouTube）提取内容并生成OpenClaw Skill。
---

# Video-Learner 🎥

把视频变成可用的 Skill！

## ⚠️ 重要：使用前必读

### 依赖要求

**必须安装以下工具：**
```bash
# 安装 yt-dlp（视频下载）
pip3 install yt-dlp

# 安装 Whisper（语音识别）
pip3 install openai-whisper

# 安装 ffmpeg（音视频处理）
brew install ffmpeg

# 安装 node（抖音下载需要）
brew install node
```

**必须先安装依赖 skill：**
```bash
npx clawhub install douyin-download
```

### 重要：直接发链接给我（推荐！）

**最简单！不需要任何配置！**

- 直接把抖音/B站/YouTube 链接发给我
- 我自动处理：
  1. **下载视频** - 用 yt-dlp 或 douyin-download
  2. **语音识别** - 用本地 Whisper 转文字
  3. **LLM 分析** - 用我的能力分析内容
  4. **生成 Skill** - 生成 SKILL.md
  5. **自动保存** - 保存到 skills/ 目录

---

## 技术说明

| 组件 | 运行方式 |
|------|----------|
| **视频下载** | yt-dlp / douyin-download（本地） |
| **语音识别** | OpenAI Whisper（本地） |
| **LLM 分析** | OpenClaw 自身能力（无需 API Key） |
| **存储** | ~/.openclaw/workspace/skills/ |

**不需要额外配置 API Key！**

---

## 支持平台

- 🎵 **抖音** - 无水印视频下载 + 语音识别
- 📺 **B站** - 音频提取 + 语音识别  
- 🎬 **YouTube** - 音频提取 + 语音识别

## 我会做什么（完整流程）

当你发视频链接给我时，我会：

1. **获取标题** - 视频的完整标题
2. **下载视频** - 用 yt-dlp 或 douyin-download
3. **语音识别** - 用本地 Whisper 把视频声音转成文字
4. **内容分析** - 用我的 LLM 能力分析视频内容：
   - 视频在讲什么
   - 核心知识点（3-5条）
   - 适用人群
   - 难度等级
5. **展示给你** - 分析结果展示，询问确认
6. **生成 Skill** - 确认后生成完整 SKILL.md
7. **自动保存** - 保存到 skills/ 目录

---

## 使用方法

### 方式1：直接发给我（推荐！）

```
发视频链接给我 → 我展示分析结果 → 你确认 → 自动生成 Skill
```

支持的链接格式：
```
抖音：https://v.douyin.com/xxx
B站：https://www.bilibili.com/video/BVxxx/
YouTube：https://youtube.com/watch?v=xxx
```

### 方式2：手动运行脚本

```bash
python3 ~/.openclaw/workspace/scripts/video-learner.py "视频链接"
```

---

## 常见问题

**Q: 需要配置 API Key 吗？**
A: 不需要！我用我的 LLM 能力处理。

**Q: 下载失败怎么办？**
A: 直接发链接给我，我帮你处理！

**Q: 每个 OpenClaw 都能这样用吗？**
A: 是的，每个 OpenClaw 都有自己的 AI 能力！

---

## 安全设计

1. **不直接记忆** - 知识点存在 Skill 文件里，不写基础记忆
2. **来源标记** - 每个 Skill 标明来源视频
3. **确认机制** - 分析结果展示给你，确认后才生成
4. **分开存储** - Skills 存单独目录，不影响基础能力

---

## 总结

**直接发视频链接给我，我帮你完成下载→识别→分析→生成 Skill 的全部流程！**