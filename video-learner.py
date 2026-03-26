#!/usr/bin/env python3
"""
Video-Learner - 视频转Skill工具（整合版 + 自动保存）
支持抖音/B站/YouTube，自动安装Skill
"""

import subprocess
import whisper
import requests
import os
import sys
import json

# 输出目录
SKILLS_DIR = os.path.expanduser("~/.openclaw/workspace/skills")

# LLM 配置（可选，用于生成Skill）
MINIMAX_API_KEY = os.environ.get("MINIMAX_API_KEY", "")
LLM_PROVIDER = os.environ.get("LLM_PROVIDER", "minimax")

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

def get_video_title(url):
    result = subprocess.run(
        ["yt-dlp", "--get-title", url],
        capture_output=True, text=True, timeout=30
    )
    return result.stdout.strip().split('\n')[0]

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

def generate_skill_with_llm(text, title):
    """用LLM生成Skill（如果配置了API Key）"""
    if not MINIMAX_API_KEY:
        return None
    
    prompt = f"""生成SKILL.md文件，包含：
1. 技能名称
2. 简短描述
3. 功能列表(5条)
4. 使用示例(对话形式)

视频标题：{title}
内容：{text[:3000]}"""

    try:
        resp = requests.post(
            "https://api.minimax.chat/v1/text/chatcompletion_v2",
            headers={
                "Authorization": f"Bearer {MINIMAX_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "MiniMax-M2.5",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 2000
            },
            timeout=30
        )
        data = resp.json()
        if "choices" in data and len(data["choices"]) > 0:
            return data["choices"][0]["message"]["content"]
    except:
        pass
    return None

def save_skill(content, skill_name):
    """自动安装Skill到skills目录"""
    skill_path = os.path.join(SKILLS_DIR, skill_name, "SKILL.md")
    os.makedirs(os.path.dirname(skill_path), exist_ok=True)
    with open(skill_path, "w", encoding="utf-8") as f:
        f.write(content)
    return skill_path

def main():
    print_banner()
    
    if not check_dependencies():
        sys.exit(1)
    
    # 检查参数
    if len(sys.argv) < 2:
        print("用法: python3 video-learner.py <视频链接> [Skill名称]")
        sys.exit(1)

    url = sys.argv[1]
    skill_name = sys.argv[2] if len(sys.argv) > 2 else "auto-skill"

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

    # 如果配置了 LLM，自动生成并保存 Skill
    if MINIMAX_API_KEY:
        print("🤖 生成Skill...")
        skill_content = generate_skill_with_llm(text, title)
        if skill_content:
            print("💾 保存Skill...")
            path = save_skill(skill_content, skill_name)
            print(f"\n✅ 完成！Skill已安装: {path}")
            print("💡 以后可以直接使用这个技能了！")
        else:
            print("⚠️ Skill生成失败")
    else:
        print("\n✅ 识别完成！")
        print(f"📝 内容预览：{text[:200]}...")
        print("\n💡 如果需要生成Skill，请设置 MINIMAX_API_KEY 环境变量")

if __name__ == "__main__":
    main()