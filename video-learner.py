#!/usr/bin/env python3
"""
Video-Learner - 视频转Skill工具（整合版）
支持抖音/B站/YouTube，抖音下载已内置
"""

import subprocess
import whisper
import os
import sys

# 输出目录
SKILLS_DIR = os.path.expanduser("~/.openclaw/workspace/skills")

def check_dependencies():
    """检查依赖"""
    # 检查 yt-dlp
    try:
        subprocess.run(["yt-dlp", "--version"], capture_output=True, timeout=5)
    except:
        print("❌ 错误: 请安装 yt-dlp")
        print("   运行: pip3 install yt-dlp")
        return False
    
    # 检查 ffmpeg
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, timeout=5)
    except:
        print("❌ 错误: 请安装 ffmpeg")
        print("   运行: brew install ffmpeg")
        return False
    
    # 检查 Node.js（用于 douyin-download）
    try:
        subprocess.run(["node", "--version"], capture_output=True, timeout=5)
    except:
        print("❌ 错误: 请安装 Node.js")
        print("   运行: brew install node")
        return False
    
    return True

def get_video_title(url):
    """获取视频标题"""
    result = subprocess.run(
        ["yt-dlp", "--get-title", url],
        capture_output=True, text=True, timeout=30
    )
    return result.stdout.strip().split('\n')[0]

def is_douyin(url):
    """判断是否是抖音链接"""
    return "douyin.com" in url

def download_douyin(url, output):
    """用内置 douyin-download 下载抖音"""
    script = os.path.join(os.path.dirname(__file__), "douyin-download", "douyin.js")
    result = subprocess.run(
        ["node", script, "download", url, "-o", output],
        capture_output=True, timeout=120
    )
    return result.returncode == 0

def download_normal(url, output):
    """用 yt-dlp 下载普通视频"""
    result = subprocess.run(
        ["yt-dlp", "-f", "30280", url, "-o", output],
        capture_output=True, timeout=60
    )
    return result.returncode == 0

def download_video(url, output):
    """根据平台选择下载方式"""
    os.makedirs(output, exist_ok=True)
    
    if is_douyin(url):
        print("📥 抖音视频，使用内置下载器...")
        return download_douyin(url, output)
    else:
        print("📥 B站/YouTube视频，使用 yt-dlp...")
        return download_normal(url, output)

def transcribe(audio_path, model_size="small"):
    """Whisper语音识别"""
    model = whisper.load_model(model_size)
    result = model.transcribe(audio_path, language="zh", fp16=False)
    return result["text"]

def save_skill(content, skill_name):
    """自动安装Skill"""
    skill_path = os.path.join(SKILLS_DIR, skill_name, "SKILL.md")
    os.makedirs(os.path.dirname(skill_path), exist_ok=True)
    with open(skill_path, "w", encoding="utf-8") as f:
        f.write(content)
    return skill_path

def main():
    print("🤖 Video-Learner - 视频转Skill工具")
    
    # 检查依赖
    if not check_dependencies():
        sys.exit(1)
    
    # 检查参数
    if len(sys.argv) < 2:
        print("用法: python3 video-learner.py <视频链接> [Skill名称]")
        sys.exit(1)

    url = sys.argv[1]
    name = sys.argv[2] if len(sys.argv) > 2 else "auto-skill"

    # 获取标题
    print(f"📥 获取视频: {url}")
    try:
        title = get_video_title(url)
        print(f"📌 标题: {title}")
    except Exception as e:
        print(f"❌ 获取标题失败: {e}")
        sys.exit(1)

    # 下载视频
    output = f"/tmp/video-download-{os.getpid()}"
    print("⬇️ 下载视频...")
    if not download_video(url, output):
        print("❌ 下载失败")
        sys.exit(1)

    # 查找下载的文件
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

    print(f"\n✅ 完成！识别内容：")
    print(text[:500] + "...")

if __name__ == "__main__":
    main()