---
name: video-learner
description: 把抖音/B站/YouTube视频变成可调用的OpenClaw Skill。
---

# Video-Learner 🎥

把视频变成可用的 Skill！

## 快速开始

**直接把视频链接发给我，我自动处理全部流程！**

支持的平台：
- 🎵 抖音
- 📺 B站  
- 🎬 YouTube

---

## 我会做什么

当你发视频链接给我时，我会：

1. **下载视频** - 获取视频内容
2. **语音识别** - 用 Whisper 把音频转成文字
3. **LLM 分析** - 用我的能力分析内容：
   - 核心知识点
   - 适用人群
   - 难度等级
4. **展示给你** - 确认分析结果
5. **生成 Skill** - 创建 SKILL.md
6. **自动保存** - 安装到 skills/ 目录

---

## 使用方式

发视频链接给我就行：

```
发给我：https://v.douyin.com/xxx
或：https://www.bilibili.com/video/BVxxx/
或：https://youtube.com/watch?v=xxx
```

我会自动处理并告诉你结果。

---

## 技术说明

| 组件 | 说明 |
|------|------|
| 视频下载 | yt-dlp / douyin-download |
| 语音识别 | 本地 Whisper（无需 API） |
| LLM 分析 | **我的能力**，无需额外 Key |
| 存储 | ~/.openclaw/workspace/skills/ |

**不需要配置任何 API Key！**

---

## 生成的 Skill

生成的 Skill 会：
- 包含视频的核心知识点
- 标明来源和难度
- 可直接调用回答相关问题

---

## 安全设计

1. **不直接记忆** - 知识点存在 Skill 文件里
2. **用户确认** - 分析结果展示后才生成
3. **来源标记** - 每个 Skill 标明出处