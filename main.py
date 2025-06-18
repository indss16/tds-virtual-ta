from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # ✅ ADD THIS
from pydantic import BaseModel
from typing import Optional
import json

app = FastAPI()

# ✅ ALLOW ALL ORIGINS FOR TESTING (you can restrict later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the data we scraped earlier
with open("scraper/discourse_data.json", encoding="utf-8") as f:
    discourse_data = json.load(f)

# Define the format for incoming questions
class QuestionPayload(BaseModel):
    question: str
    image: Optional[str] = None  # For future use, we ignore image for now

# Define your API endpoint
@app.post("/api/")
async def answer_question(payload: QuestionPayload):
    question = payload.question.lower()

    # Match using keyword search
    matched = []
    for post in discourse_data:
        if any(word in post["content"].lower() for word in question.split()):
            matched.append(post)
            if len(matched) >= 2:
                break

    if not matched:
        return {
            "answer": "Sorry, I couldn’t find anything helpful. A TA will reply soon.",
            "links": []
        }

    return {
        "answer": matched[0]["content"][:500] + "...",
        "links": [
            {"url": post["url"], "text": post["title"]}
            for post in matched
        ]
    }

@app.get("/")
def root():
    return {"message": "Your FastAPI app is running successfully!"}
