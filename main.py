from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from markitdown import MarkItDown
from groq import Groq
import os
import tempfile

#python -m uvicorn main:app --reload

app = FastAPI()

# Allow your HTML file to talk to this Python server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key="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")

@app.post("/analyze")
async def analyze_resume(file: UploadFile = File(...)):
    suffix = os.path.splitext(file.filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    # Convert to text
    md = MarkItDown()
    resume_text = md.convert(tmp_path).text_content
    os.remove(tmp_path)

    # Groq AI Logic
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": f"Analyze this resume: {resume_text}"}],
        model="llama-3.3-70b-versatile",
    )
    
    return {"analysis": chat_completion.choices[0].message.content}