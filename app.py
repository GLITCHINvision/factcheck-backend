from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import (
    fetch_news,
    fetch_scholar_data,
    summarize_sources,
    fetch_real_news  
)

app = Flask(__name__)
CORS(app)

@app.route("/fact-check", methods=["POST"])
def fact_check():
    data = request.get_json()
    query = data.get("query")
    mode = data.get("mode", "llm")  

    if not query:
        return jsonify({"answer": " No query received."}), 400

    if mode == "verified":
        news_data = fetch_real_news(query)
        if not news_data:
            return jsonify({"answer": " No real sources found."})
        return jsonify({"answer": "\n".join(news_data)})

    
    news_data = fetch_news(query)
    scholar_data = fetch_scholar_data(query)
    summary = summarize_sources(query, news_data, scholar_data)
    return jsonify({"answer": summary})

if __name__ == "__main__":
    app.run(debug=True)

