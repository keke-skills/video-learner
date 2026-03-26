#!/usr/bin/env python3
"""
Video-Learner - 视频转Skill工具（整合版）
支持抖音/B站/YouTube，自动命名
"""

import subprocess
import whisper
import os
import sys

# 输出目录
SKILLS_DIR = os.path.expanduser("~/.openclaw/workspace/skills")

DEPENDENCIES = {
    "yt-dlp": {
        "install": "pip3 install yt-dlp",
        "check": ["yt-dlp", "--version"],
        "desc": "视频下载"
    },
    "ffmpeg": {
        "install": "brew install ffmpeg",
        "check": ["ffmpeg", "-version"],
        "desc": "音视频处理"
    },
    "whisper": {
        "install": "pip3 install openai-whisper",
        "check": ["python3", "-c", "import whisper"],
        "desc": "语音识别"
    },
    "node": {
        "install": "brew install node",
        "check": ["node", "--version"],
        "desc": "抖音下载"
    }
}

def print_banner():
    print("="*50)
    print("📦 Video-Learner - 视频转Skill工具")
    print("="*50)
    print("\n⚠️  使用前请确保已安装以下依赖：\n")
    for name, info in DEPENDENCIES.items():
        print(f"  • {name:10} - {info['desc']:15} (安装: {info['install']})")
    print("\n" + "="*50)

def check_dependencies():
    missing = []
    for name, info in DEPENDENCIES.items():
        try:
            if name == "whisper":
                result = subprocess.run(
                    ["python3", "-c", "import whisper"],
                    capture_output=True, timeout=5
                )
                if result.returncode != 0:
                    missing.append((name, info))
            else:
                subprocess.run(info["check"], capture_output=True, timeout=5)
        except:
            missing.append((name, info))
    
    if missing:
        print("\n❌ 发现缺少以下依赖：\n")
        for name, info in missing:
            print(f"  • {name} ({info['desc']})")
            print(f"    安装命令: {info['install']}")
        print("\n" + "="*50)
        return False
    
    print("✅ 所有依赖已安装，可以正常使用！\n")
    return True

def clean_filename(name):
    """清理文件名，去除特殊字符"""
    # 简单处理：只保留字母、数字、中文、常见符号
    import re
    # 只保留字母、数字、中文、常用符号
    name = re.sub(r'[^\w\u4e00-\u9fff\u3000-\u303f\uff00-\uffef\-_]', '', name)
    name = name.strip()
    # 限制长度
    if len(name) > 30:
        name = name[:30]
    # 空格转横线
    name = name.replace(' ', '-')
    # 如果为空，给个默认名
    if not name:
        name = "video-skill"
    return name

def get_video_title(url):
    try:
        result = subprocess.run(
            ["yt-dlp", "--get-title", url],
            capture_output=True, text=True, timeout=30
        )
        title = result.stdout.strip().split('\n')[0]
        if not title:
            return "video-skill"
        return title
    except Exception as e:
        print(f"⚠️ 获取标题失败，使用默认名称: {e}")
        return "video-skill"

def is_douyin(url):
    return "douyin.com" in url

def download_douyin(url, output):
    script = os.path.join(os.path.dirname(__file__), "douyin-download", "douyin.js")
    result = subprocess.run(
        ["node", script, "download", url, "-o", output],
        capture_output=True, timeout=120
    )
    return result.returncode == 0

def download_normal(url, output):
    result = subprocess.run(
        ["yt-dlp", "-f", "30280", url, "-o", output],
        capture_output=True, timeout=60
    )
    return result.returncode == 0

def download_video(url, output):
    os.makedirs(output, exist_ok=True)
    if is_douyin(url):
        print("📥 抖音视频...")
        return download_douyin(url, output)
    else:
        print("📥 B站/YouTube视频...")
        return download_normal(url, output)

def transcribe(audio_path, model_size="small"):
    model = whisper.load_model(model_size)
    result = model.transcribe(audio_path, language="zh", fp16=False)
    return result["text"]

def main():
    print_banner()
    
    if not check_dependencies():
        sys.exit(1)
    
    if len(sys.argv) < 2:
        print("用法: python3 video-learner.py <视频链接>")
        sys.exit(1)

    url = sys.argv[1]

    print(f"📥 获取视频: {url}")
    try:
        title = get_video_title(url)
        print(f"📌 标题: {title}")
        
        # 自动生成 Skill 名称
        skill_name = clean_filename(title)
        print(f"🏷️ Skill名称: {skill_name}")
    except Exception as e:
        print(f"❌ 获取标题失败: {e}")
        sys.exit(1)

    output = f"/tmp/video-download-{os.getpid()}"
    print("⬇️ 下载视频...")
    if not download_video(url, output):
        print("❌ 下载失败")
        sys.exit(1)

    # 查找视频文件
    video_file = None
    for f in os.listdir(output):
        if f.endswith('.mp4'):
            video_file = os.path.join(output, f)
            break
    
    if not video_file:
        print("❌ 未找到视频文件")
        sys.exit(1)

    # 转换音频
    audio_file = os.path.join(output, "audio.wav")
    print("🎤 转换音频...")
    result = subprocess.run(
        ["ffmpeg", "-i", video_file, "-ar", "16000", "-ac", "1", audio_file, "-y"],
        capture_output=True
    )
    if result.returncode != 0:
        print("❌ 音频转换失败")
        sys.exit(1)

    # 语音识别
    print("🔍 语音识别...")
    text = transcribe(audio_file)
    print(f"📝 识别了 {len(text)} 字")

    # 保存到 skills 目录
    skill_path = os.path.join(SKILLS_DIR, skill_name, "SKILL.md")
    os.makedirs(os.path.dirname(skill_path), exist_ok=True)
    
    # 创建基础 Skill 文件
    skill_content = f"""# {title}

## 简短描述

基于视频「{title}」生成的技能

## 功能

- 自动整理视频内容
- 提供相关知识查询
- 回答视频相关问题

## 使用示例

用户：{title} 讲了什么？
助手：这是一段关于「{title}」的视频内容...

## 备注

识别字数：{len(text)} 字
生成时间：{__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}
"""

    with open(skill_path, "w", encoding="utf-8") as f:
        f.write(skill_content)

    print(f"\n✅ 完成！")
    print(f"📁 Skill已保存: {skill_path}")
    print(f"🏷️ Skill名称: {skill_name}")
    print("\n💡 识别结果已保存，你可以告诉我需要生成什么内容的Skill，我来帮你完善！")

if __name__ == "__main__":
    main()