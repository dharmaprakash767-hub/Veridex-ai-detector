import os import requests from fastapi import FastAPI, File, UploadFile from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

Frontend se connect karne ke liye CORS
app.add_middleware( CORSMiddleware, allow_origins=[""], allow_methods=[""], allow_headers=["*"], )

API_USER = os.environ.get('API_USER') API_SECRET = os.environ.get('API_SECRET')

@app.get("/") def home(): return {"message": "Deepfake & AI Content Detector Backend Active!"}

@app.post("/detect-image/") async def detect_image(file: UploadFile = File(...)): image_bytes = await file.read()

# Sightengine AI Detection Model Call
response = requests.post(
    'https://api.sightengine.com/1.0/check.json',
    files={'media': image_bytes},
    data={
        'models': 'genai', # Checks for DALL-E, Midjourney, Deepfakes
        'api_user': API_USER,
        'api_secret': API_SECRET
    }
)
result = response.json()
# Extract AI Probability
ai_score = 0
if 'type' in result and 'ai_generated' in result['type']:
    ai_score = result['type']['ai_generated'] * 100
return {
    "filename": file.filename,
    "ai_percentage": round(ai_score, 2),
    "is_ai": ai_score > 50,
    "status": "Success" if response.status_code == 200 else "Failed"
}
