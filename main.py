from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import torch
import os
from transformers_interpret import SequenceClassificationExplainer

# Cache directories are set in Dockerfile

app = FastAPI(title="LightGuard API", description="Production LLM Safety Filter")
JAILBREAK_THRESHOLD = 0.90

# Serve React build files
app.mount("/static", StaticFiles(directory="frontend/build/static"), name="static")

# Load model
print("Loading LightGuard classification model...")

# Try to load from local files first, fallback to HF Hub if needed
local_model_path = "lightguard_final_model"
if os.path.exists(local_model_path):
    print(f"Loading model from local path: {local_model_path}")
    try:
        tokenizer = AutoTokenizer.from_pretrained(local_model_path, local_files_only=True)
        model = AutoModelForSequenceClassification.from_pretrained(local_model_path, local_files_only=True)
    except Exception as e:
        print(f"Local loading failed: {e}")
        print("Falling back to Hugging Face Hub...")
        tokenizer = AutoTokenizer.from_pretrained("yahmed124/lightguard-model")
        model = AutoModelForSequenceClassification.from_pretrained("yahmed124/lightguard-model")
else:
    print("Local model not found, loading from Hugging Face Hub...")
    tokenizer = AutoTokenizer.from_pretrained("yahmed124/lightguard-model")
    model = AutoModelForSequenceClassification.from_pretrained("yahmed124/lightguard-model")
classifier = pipeline("text-classification", model=model, tokenizer=tokenizer, device=-1, top_k=None)
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
        
        # Add explainability only for unsafe prompts
        explanation = None
        if not is_safe:
            # Initialize explainer
            explainer = SequenceClassificationExplainer(model, tokenizer)
            # Get word attributions (this may take a moment)
            word_attributions = explainer(request.prompt)
            # Extract top 3 most suspicious phrases
            top_attributions = sorted(word_attributions, key=lambda x: x[1], reverse=True)[:3]
            explanation = " | ".join([f"'{word}' ({score:.2f})" for word, score in top_attributions])
        
        return {
            "safe": is_safe,
            "jailbreak_score": jailbreak_score,
            "message": None if is_safe else "Blocked: High jailbreak probability.",
            "explanation": explanation  # New field
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
async def serve_react_app():
    return FileResponse("frontend/build/index.html")

@app.get("/{full_path:path}")
async def catch_all(full_path: str):
    return FileResponse("frontend/build/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)