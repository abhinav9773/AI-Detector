import os
import dotenv
from fastapi import FastAPI, HTTPException
import requests
import openai  # ✅ Import OpenAI

# ✅ Load environment variables
dotenv.load_dotenv(dotenv_path=".env")

# ✅ Load API Keys
GOOGLE_FACTCHECK_API_KEY = os.getenv("GOOGLE_FACTCHECK_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ✅ Debugging: Check if API keys are loaded
print("Google API Key:", "Loaded" if GOOGLE_FACTCHECK_API_KEY else "NOT FOUND")
print("OpenAI API Key:", "Loaded" if OPENAI_API_KEY else "NOT FOUND")

if not GOOGLE_FACTCHECK_API_KEY:
    raise ValueError("Google API Key is missing! Set GOOGLE_FACTCHECK_API_KEY in your .env file.")
if not OPENAI_API_KEY:
    raise ValueError("OpenAI API Key is missing! Set OPENAI_API_KEY in your .env file.")

app = FastAPI()

def verify_news_with_google(news_url):
    """Checks if the news has been fact-checked by Google Fact-Check API."""
    try:
        endpoint = f"https://factchecktools.googleapis.com/v1alpha1/claims:search?query={news_url}&key={GOOGLE_FACTCHECK_API_KEY}"
        response = requests.get(endpoint)
        response_json = response.json()
        
        if "claims" in response_json and response_json["claims"]:
            return response_json["claims"]  # ✅ Return all claims found
        
        return None  # No fact-checking results
    
    except Exception as e:
        return {"error": f"Google API Error: {str(e)}"}

def analyze_news_with_openai(news_url):
    """Uses OpenAI to analyze the news and check its credibility."""
    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)  # ✅ Updated OpenAI client
        response = client.chat.completions.create(  # ✅ Updated method
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI that detects fake news."},
                {"role": "user", "content": f"Analyze this news article and determine if it seems reliable or fake: {news_url}"}
            ]
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        return {"error": f"OpenAI API Error: {str(e)}"}

@app.get("/")
def read_root():
    return {"message": "Hello, TruthLens API is running!"}

@app.post("/check-news")
def check_news(data: dict):
    news_url = data.get("url")
    
    if not news_url:
        raise HTTPException(status_code=400, detail="URL is required")
    
    # ✅ Step 1: Try Google Fact-Check API
    google_result = verify_news_with_google(news_url)
    
    # ✅ Step 2: If no Google results, use OpenAI
    if not google_result:
        openai_analysis = analyze_news_with_openai(news_url)
        return {
            "url": news_url,
            "google_fact_check": "No results found",
            "openai_analysis": openai_analysis
        }
    
    return {
        "url": news_url,
        "google_fact_check": google_result
    }
