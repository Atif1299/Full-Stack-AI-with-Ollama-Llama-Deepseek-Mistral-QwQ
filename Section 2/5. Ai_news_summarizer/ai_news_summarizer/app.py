from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import requests
import os
import json

app = FastAPI()

# Serve static files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# API Configuration
NEWS_API_URL = "https://newsapi.org/v2/top-headlines"
NEWS_API_KEY = "NEWS_API_KEY"  # Replace with your API key
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5"  # Using Qwen2.5 for summarization

@app.get("/")
def serve_homepage():
    """ Serve the index.html file when accessing the root URL """
    return FileResponse(os.path.join("static", "index.html"))

@app.get("/fetch_news")
def fetch_and_summarize_news(category: str = Query("technology")):
    """ Fetches latest news articles and summarizes them using Ollama """
    headers = {"Authorization": f"Bearer {NEWS_API_KEY}"}
    params = {"category": category, "language": "en", "apiKey": NEWS_API_KEY}
    
    try:
        news_response = requests.get(NEWS_API_URL, params=params, headers=headers)
        if news_response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to fetch news articles")

        news_data = news_response.json()
        if "articles" not in news_data or not news_data["articles"]:
            return {"summary": "No news articles found for this category."}

        # Extract top 3 articles
        articles = news_data["articles"][:3]
        news_text = "\n".join([f"- {article['title']} ({article['source']['name']})" for article in articles])

        # Send news text to Ollama for summarization
        ollama_response = requests.post(
            OLLAMA_URL,
            json={"model": MODEL_NAME, "prompt": f"Summarize these news headlines:\n{news_text}", "stream": False},
        )

        # Log response
        print("Ollama Response:", ollama_response.text)

        # Ensure valid JSON response
        response_data = ollama_response.text.strip()
        try:
            json_response = json.loads(response_data)
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail=f"Invalid JSON response from Ollama: {response_data}")

        summary = json_response.get("response", "No summary available.")
        return {"summary": summary, "articles": articles}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch or summarize news: {str(e)}")

# Run the API server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)








