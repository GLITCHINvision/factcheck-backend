import requests
import os
from dotenv import load_dotenv
from transformers import pipeline


load_dotenv()


NEWS_API_KEY = os.getenv("NEWS_API_KEY")


try:
    summarizer = pipeline("summarization", model="Falconsai/text_summarization")

except Exception as e:
    summarizer = None
    print(f" Failed to load summarizer: {e}")



def fetch_real_news(query):
    if not NEWS_API_KEY:
        return [" NEWS_API_KEY not found in .env"]

    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "apiKey": NEWS_API_KEY,
        "language": "en",
        "pageSize": 5,
    }

    try:
        res = requests.get(url, params=params, timeout=10)
        res.raise_for_status()
        articles = res.json().get("articles", [])
        if not articles:
            return [" No relevant news found."]
        return [f"{a['source']['name']} says: {a['title']}" for a in articles]
    except requests.exceptions.RequestException as e:
        return [f" Error fetching news: {str(e)}"]



def fetch_news(query):
    return [
        f"TimesNow reports: '{query}' was said in parliament.",
        f"The Wire disagrees: PM made no such statement recently."
    ]


def fetch_scholar_data(query):
    return [
        f"MIT research says achieving '{query}' by 2047 is optimistic.",
        f"India Energy Outlook 2023 supports partial feasibility."
    ]



def summarize_sources(query, news, scholar):
    all_sources = "\n".join(news + scholar)

    prompt = f"""
Question: {query}
Sources:
{all_sources}

Answer the question above factually, using only the sources provided.
Keep it short, neutral, and clear.
"""

    if summarizer is None:
        return " Summarizer model is not available."

    try:
        result = summarizer(prompt, max_length=150, min_length=50, do_sample=False)
        return result[0]["summary_text"]
    except Exception as e:
        return f" Failed to summarize: {str(e)}"
