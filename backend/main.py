import os
from fastapi import FastAPI, Depends
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi_clerk_auth import ClerkConfig, ClerkHTTPBearer
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

clerk_config = ClerkConfig(jwks_url=os.getenv("CLERK_JWKS_URL"))
clerk_guard = ClerkHTTPBearer(clerk_config)

@app.get("/api/generate")
def generate_linkedin_post(creds=Depends(clerk_guard)):
    user_id = creds.decoded["sub"]
    # Khởi tạo OpenAI client
    client = OpenAI()
    # Tạo prompt cho AI
    prompt = [
        {
            "role": "user",
            "content": (
                "Write a high-quality LinkedIn post for professionals in AI and technology.\n\n"
                "Topic: The importance of learning AI in 2025\n\n"
                "Guidelines:\n"
                "- Target audience: AI engineers, data scientists, founders, and tech professionals\n"
                "- Tone: Conversational, insightful, and slightly opinionated\n"
                "- Structure:\n"
                "  1. Strong hook in the first 1–2 lines\n"
                "  2. A short personal insight or observation\n"
                "  3. 2–3 practical takeaways or lessons\n"
                "  4. A thoughtful call-to-action at the end\n"
                "- Use line breaks for readability\n"
                "- Use 2–4 relevant emojis (AI, tech, learning)\n"
                "- Avoid marketing fluff and generic advice\n\n"
                "The post should feel authentic and written by a real AI practitioner."
            )
        }
    ]

    # Gọi OpenAI API với streaming
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=prompt,
        stream=True
    )
    def event_stream():
        for chunk in stream:
            delta = chunk.choices[0].delta
            if delta and delta.content:
                text = delta.content
                lines = text.split("\n")

                for line in lines:
                    yield f"data: {line}\n\n"
    # Trả về streaming response
    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache"}
    )