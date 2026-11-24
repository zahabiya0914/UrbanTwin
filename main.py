from pathlib import Path
import os
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent
app = FastAPI(title="UrbanTwin AI", description="Smart city traffic digital twin with optional LLM assistance", version="1.0.0")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    context: Optional[dict] = None

class OptimizeRequest(BaseModel):
    mode: str = "adaptive"
    traffic: int = Field(default=58, ge=0, le=100)
    emergency: bool = False
    weather: str = "clear"

@app.get("/")
def home():
    return FileResponse(BASE_DIR / "templates" / "index.html")

@app.get("/api/health")
def health():
    return {"status": "ok", "llm_configured": bool(os.getenv("OPENAI_API_KEY")), "project": "UrbanTwin AI"}

@app.post("/api/optimize")
def optimize(req: OptimizeRequest):
    """A transparent demo policy; replace with SUMO/RL integration for research deployment."""
    traffic = req.traffic
    if req.emergency:
        return {"strategy": "Emergency green corridor", "green_seconds": 45, "cycle_seconds": 60,
                "priority": "Emergency vehicle", "reason": "Temporarily prioritize the emergency route and restore normal timing after it passes."}
    if req.mode == "fixed":
        return {"strategy": "Fixed-time baseline", "green_seconds": 30, "cycle_seconds": 90,
                "priority": "Balanced phases", "reason": "Uses a constant 30-second green phase regardless of current demand; useful as a baseline."}
    green = max(20, min(55, round(20 + traffic * 0.35)))
    return {"strategy": "Adaptive demand-based timing", "green_seconds": green, "cycle_seconds": 90,
            "priority": "Highest queue / demand", "reason": f"Demo policy allocates {green} seconds of green time based on a traffic-demand score of {traffic}/100. This is a rule-based baseline, not a trained reinforcement-learning model."}

@app.post("/api/chat")
def chat(req: ChatRequest):
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    if api_key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            context = req.context or {}
            system = (
                "You are UrbanTwin AI, an assistant for a student smart-city traffic digital-twin demo. "
                "Give concise, technically useful explanations about traffic simulation, adaptive signals, emergency routing, "
                "metrics, and evaluation. Be explicit when values are simulated, not real-world observations. "
                "Do not claim the demo uses trained reinforcement learning unless the user has implemented it. "
                f"Current simulation context: {context}"
            )
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "system", "content": system}, {"role": "user", "content": req.message}],
                temperature=0.4,
                max_tokens=450,
            )
            return {"reply": response.choices[0].message.content or "I couldn't generate a response.", "provider": "openai", "model": model}
        except Exception as exc:
            return {"reply": f"The LLM request failed ({type(exc).__name__}). Check your API key, model name, and internet connection. The simulator itself can still run without the LLM.", "provider": "fallback", "model": None}

    msg = req.message.lower()
    if any(word in msg for word in ["emergency", "ambulance", "fire", "priority"]):
        reply = "For this demo, enable Emergency Mode to create a green corridor. A production design should estimate route travel time, coordinate adjacent intersections, and safely restore normal phases after the vehicle passes. The current feature is a simplified simulation, not a connection to real emergency services."
    elif any(word in msg for word in ["adaptive", "traffic light", "signal", "fixed"]):
        reply = "Adaptive control changes green time in response to measured demand, while the fixed-time baseline uses the same schedule regardless of queues. Compare average wait, estimated queue length, throughput, and stops over repeated runs with the same demand seed. The dashboard's adaptive policy is a transparent rule-based demo, not trained reinforcement learning."
    elif any(word in msg for word in ["predict", "forecast", "prediction"]):
        reply = "The dashboard's forecast is a lightweight heuristic based on the current synthetic demand level. For a research-grade forecast, collect time-stamped traffic counts, create lag and calendar features, split data chronologically, and compare a persistence baseline with models such as Random Forest or XGBoost using MAE/RMSE."
    elif any(word in msg for word in ["metric", "evaluate", "research", "compare"]):
        reply = "Recommended evaluation: run fixed-time and adaptive modes against identical demand scenarios at least 20 times. Report mean waiting time, average queue length, throughput, emergency-route delay, and variability. Include a baseline, describe your synthetic data, and avoid treating simulated results as evidence about a real city."
    else:
        reply = "I'm UrbanTwin AI. I can explain the simulation, adaptive signal timing, emergency priority, traffic forecasts, or how to evaluate fixed-time versus adaptive control. This local demo is running without an LLM API key; add OPENAI_API_KEY to enable model-powered responses."
    return {"reply": reply, "provider": "built-in demo assistant", "model": None}
