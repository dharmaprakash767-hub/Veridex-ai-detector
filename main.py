import os
import requests
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

API_USER = os.environ.get('API_USER')
API_SECRET = os.environ.get('API_SECRET')

@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("index.html", "r") as f:
        return f.read()

@app.post("/predict")
async def predict_image(file: UploadFile = File(...)):
    if not API_USER or not API_SECRET:
        return {"error": "API credentials missing."}

    payload = {
        'models': 'genai',
        'api_user': API_USER,
        'api_secret': API_SECRET
    }
    
    files = {'media': (file.filename, await file.read(), file.content_type)}
    
    response = requests.post('https://api.sightengine.com/1.0/check.json', data=payload, files=files)
    result = response.json()
    
    if result.get('status') == 'success':
        ai_score = result.get('type', {}).get('ai_generated', 0)
        return {"ai_score": ai_score}
    else:
        return {"error": "Failed to process image.", "details": result}
        
