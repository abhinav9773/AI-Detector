import os
import dotenv
import traceback
import requests
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Load environment variables
dotenv.load_dotenv()

GOOGLE_FACTCHECK_API_KEY = os.getenv("GOOGLE_FACTCHECK_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not GOOGLE_FACTCHECK_API_KEY:
    raise ValueError("Google API Key is missing! Set GOOGLE_FACTCHECK_API_KEY in your .env file.")
if not OPENAI_API_KEY:
    raise ValueError("OpenAI API Key is missing! Set OPENAI_API_KEY in your .env file.")

# Initialize FastAPI app
app = FastAPI()

# Enable CORS (allow frontend to call API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500"],  # Allow frontend access
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Handle preflight requests
@app.options("/api/news/analyze")
async def preflight():
    return JSONResponse(status_code=200, headers={
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "*",
    })

# Root endpoint (check if server is running)
@app.get("/")
def read_root():
    return {"message": "Hello, TruthLens API is running!"}

# Function to check news credibility
def check_news_with_openai(news_text):
    url = "https://api.openai.com/v1/chat/completions"  # Ensure correct API URL
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "gpt-3.5-turbo",  # Ensure you're using a valid model
        "messages": [
            {"role": "system", "content": "Analyze the credibility of the following news and return either TRUE or FALSE."},
            {"role": "user", "content": news_text}
        ]
    }

    response = requests.post(url, headers=headers, json=payload)

    # Debugging: Print the full response
    print("🔍 OpenAI API Response:", response.status_code, response.text)

    if response.status_code == 429:
        raise HTTPException(status_code=429, detail="API limit exceeded. Try again later.")
    elif response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=f"OpenAI API Error: {response.text}")

    result = response.json()
    return result["choices"][0]["message"]["content"]  # Extract the answer

# Analyze news endpoint
@app.post("/api/news/analyze")
async def analyze_news(request: Request):
    try:
        data = await request.json()
        news_text = data.get("text")

        if not news_text:
            raise HTTPException(status_code=400, detail="Text is required")

        # Call OpenAI API to analyze credibility
        credibility_result = check_news_with_openai(news_text)

        return {"success": True, "result": credibility_result}

    except Exception as e:
        error_details = traceback.format_exc()  # Get full error trace
        print(f"🔥 ERROR: {error_details}")  # Print full error to terminal

        return JSONResponse(status_code=500, content={"detail": f"Server Error: {str(e)}"})
