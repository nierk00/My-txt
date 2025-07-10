import feedparser
import openai
import os
from datetime import datetime

# GPT API 키 불러오기
openai.api_key = os.getenv("OPENAI_API_KEY")

# 1. RSS 뉴스 가져오기 (IT 뉴스)
rss_url = "https://rss.etnews.com/Section902.xml"
feed = feedparser.parse(rss_url)

# 2. 최신 뉴스 3개 선택
news_items = feed.entries[:3]

print(f"📰 {datetime.now().strftime('%Y-%m-%d')} 뉴스 요약 시작!\n")

# 3. GPT로 요약하기
for i, news in enumerate(news_items, 1):
    title = news.title
    link = news.link
    description = news.get("description", "")

    prompt = f"다음 뉴스 내용을 3줄로 간단히 요약해줘:\n\n제목: {title}\n내용: {description}"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # 무료 요금제도 사용 가능
            messages=[
                {"role": "system", "content": "뉴스 요약 도우미야"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.7
        )

        summary = response['choices'][0]['message']['content'].strip()

        print(f"#{i} {title}\n링크: {link}\n요약: {summary}\n")

    except Exception as e:
        print(f"[에러] {title} 요약 실패: {e}")
