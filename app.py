from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import torch

app = FastAPI(title="LightGuard API", description="Production LLM Safety Filter")
JAILBREAK_THRESHOLD = 0.90

print("Loading LightGuard classification model...")
model_path = "./lightguard_final_model"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)
classifier = pipeline("text-classification", model=model, tokenizer=tokenizer, top_k=None)
print("Model loaded successfully.")

class PromptRequest(BaseModel):
    prompt: str

class SafetyResponse(BaseModel):
    safe: bool
    jailbreak_score: float
    message: str | None = None

@app.post("/check-safety")
async def check_safety(request: PromptRequest):
    try:
        results = classifier(request.prompt)
        jailbreak_score = next(item['score'] for item in results[0] if item['label'] == 'LABEL_1')
        is_safe = jailbreak_score < JAILBREAK_THRESHOLD
        return {
            "safe": is_safe,
            "jailbreak_score": jailbreak_score,
            "message": None if is_safe else "Blocked: High jailbreak probability."
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
async def root():
    return {"message": "LightGuard Safety API is operational."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)