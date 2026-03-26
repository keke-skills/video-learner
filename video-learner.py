#!/usr/bin/env python3
"""
Content Extractor - 视频转Skill工具（安全版）
自动从B站/YouTube视频生成OpenClaw Skill

流程：视频 → 下载 → 识别 → 分析展示 → 用户确认 → 生成 → 自动安装
"""

import subprocess
import whisper
import requests
import os
import sys

# 从环境变量读取 API Key（安全）
API_KEY = os.environ.get("MINIMAX_API_KEY", "")
MODEL = "MiniMax-M2.5"

# 获取用户目录（兼容不同机器）
SKILLS_DIR = os.path.expanduser("~/.openclaw/workspace/skills")

def check_api_key():
    """检查API Key是否设置"""
    if not API_KEY:
        print("❌ 错误: 请设置环境变量 MINIMAX_API_KEY")
        print("   运行: export MINIMAX_API_KEY='你的API Key'")
        sys.exit(1)

def get_video_title(url):
    """获取视频标题"""
    result = subprocess.run(
        ["yt-dlp", "--get-title", url],
        capture_output=True, text=True,
        timeout=30
    )
    return result.stdout.strip().split('\n')[0]

def download_audio(url, output="/tmp/video-audio.m4a"):
    """下载视频音频"""
    result = subprocess.run(
        ["yt-dlp", "-f", "30280", url, "-o", output],
        capture_output=True, timeout=60
    )
    if result.returncode != 0:
        print(f"⚠️ 下载警告: {result.stderr.decode()}")
    return output

def transcribe(audio_path, model_size="small"):
    """Whisper语音识别"""
    try:
        model = whisper.load_model(model_size)
        result = model.transcribe(audio_path, language="zh", fp16=False)
        return result["text"]
    except Exception as e:
        print(f"❌ 语音识别失败: {e}")
        sys.exit(1)

def analyze_content(text):
    """LLM分析内容 - 先展示给用户确认"""
    try:
        prompt = f"""分析以下内容，提取：
1. 核心知识点 (3-5条)
2. 适用人群
3. 难度等级

原文：{text[:3000]}"""

        resp = requests.post(
            "https://api.minimax.chat/v1/text/chatcompletion_v2",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": MODEL,
                "messages": [
                    {"role": "system", "content": "你是内容分析专家"},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 1000
            },
            timeout=30
        )
        data = resp.json()
        if "choices" in data and len(data["choices"]) > 0:
            return data["choices"][0]["message"]["content"]
        else:
            print(f"⚠️ API返回异常: {data}")
            return "分析失败"
    except Exception as e:
        print(f"⚠️ 分析出错: {e}")
        return "分析失败"

def generate_skill(text, title):
    """生成完整Skill"""
    try:
        prompt = f"""生成SKILL.md文件，包含：
1. 技能名称
2. 简短描述
3. 功能列表(5条)
4. 使用示例(对话形式)

视频标题：{title}
内容：{text[:3000]}"""

        resp = requests.post(
            "https://api.minimax.chat/v1/text/chatcompletion_v2",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": MODEL,
                "messages": [
                    {"role": "system", "content": "你是技能生成助手"},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 2000
            },
            timeout=30
        )
        data = resp.json()
        if "choices" in data and len(data["choices"]) > 0:
            return data["choices"][0]["message"]["content"]
        else:
            return "Skill生成失败"
    except Exception as e:
        return f"Skill生成失败: {e}"

def save_skill(content, skill_name):
    """自动安装Skill到skills目录"""
    skill_path = os.path.join(SKILLS_DIR, skill_name, "SKILL.md")
    os.makedirs(os.path.dirname(skill_path), exist_ok=True)
    with open(skill_path, "w", encoding="utf-8") as f:
        f.write(content)
    return skill_path

def main():
    # 检查API Key
    check_api_key()

    # 检查参数
    if len(sys.argv) < 2:
        print("用法: python3 content-extractor.py <视频链接> [Skill名称]")
        print("示例: python3 content-extractor.py 'https://www.bilibili.com/video/BVxxx/' '我的技能'")
        sys.exit(1)

    url = sys.argv[1]
    name = sys.argv[2] if len(sys.argv) > 2 else "auto-skill"

    # 步骤1: 获取标题
    print(f"📥 获取视频: {url}")
    try:
        title = get_video_title(url)
        print(f"📌 标题: {title}")
    except Exception as e:
        print(f"❌ 获取标题失败: {e}")
        sys.exit(1)

    # 步骤2: 下载音频
    print("⬇️ 下载音频...")
    audio = download_audio(url)

    # 步骤3: 语音识别
    print("🎤 语音识别...")
    text = transcribe(audio)
    print(f"📝 识别了 {len(text)} 字")

    # 步骤4: 分析内容（展示给用户确认）
    print("🔍 分析内容...")
    analysis = analyze_content(text)
    print("\n" + "="*50)
    print("📋 分析结果：")
    print(analysis)
    print("="*50)
    
    confirm = input("\n✅ 确认生成Skill? (y/n): ")
    if confirm.lower() != 'y':
        print("❌ 已取消")
        return

    # 步骤5: 生成完整Skill
    print("🤖 生成Skill...")
    skill = generate_skill(text, title)

    # 步骤6: 自动安装
    print("💾 安装Skill...")
    path = save_skill(skill, name)

    print(f"\n✅ 完成！Skill已安装: {path}")
    print("💡 以后可以直接使用这个技能了！")

if __name__ == "__main__":
    main()