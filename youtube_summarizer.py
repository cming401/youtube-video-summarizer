import json
import requests
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from urllib.parse import urlparse, parse_qs

# ========== 🔧 配置 ==========
DEEPSEEK_API_KEY = "INSERT_YOUR_DEEKSEEK_API" #Deepseek Api key, 切换成你的API key

# ============ Step 1: 提取视频ID ============
def extract_video_id(youtube_url):
    query = urlparse(youtube_url)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ['www.youtube.com', 'youtube.com']:
        if query.path == '/watch':
            return parse_qs(query.query)['v'][0]
        elif query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        elif query.path[:3] == '/v/':
            return query.path.split('/')[2]
    raise ValueError("无法解析 YouTube 链接")

# ============ Step 2: 获取字幕 ============
def fetch_captions(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        # 优先中文
        try:
            transcript = transcript_list.find_transcript(['zh-Hans', 'zh-CN', 'zh'])
        except NoTranscriptFound:
            transcript = transcript_list.find_transcript(['en'])

        fetched = transcript.fetch()
        return " ".join([entry.text for entry in fetched])

    except (TranscriptsDisabled, NoTranscriptFound) as e:
        return f"字幕获取失败: {e}"

# ============ Step 3: 调用 DeepSeek Chat 总结 ============
def summarize_with_deepseek(text, api_key):
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "你是一个善于总结视频内容的AI助手。"},
            {"role": "user", "content": f"请用中文总结以下YouTube视频字幕内容：\n{text}"}
        ],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    result = response.json()
    return result["choices"][0]["message"]["content"]

# ============ Step 4: 主函数 ============
def main():
    youtube_url = input("请输入YouTube视频链接：")
    video_id = extract_video_id(youtube_url)
    print("正在获取字幕...")
    captions = fetch_captions(video_id)

    if captions.startswith("字幕获取失败"):
        print(captions)
        return

    print("字幕获取成功，正在总结中...")
    summary = summarize_with_deepseek(captions, DEEPSEEK_API_KEY)
    print("\n📄 总结结果：\n")
    print(summary)

main()
