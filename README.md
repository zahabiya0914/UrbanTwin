# UrbanTwin AI — Smart City Digital Twin

A student-friendly MCA project prototype with an animated synthetic road network, traffic-demand controls, fixed-time vs. adaptive signal comparison, emergency-priority mode, weather effects, simulated performance metrics, and an optional LLM assistant.

## Features

- Responsive dark dashboard for desktop and mobile.
- Animated synthetic vehicles and 16 intersections on a canvas-based road grid.
- Adjustable traffic demand, weather, and signal strategy.
- Emergency-priority demonstration mode.
- Comparative metrics: average wait time, throughput, and queue length.
- FastAPI backend with `/api/health`, `/api/optimize`, and `/api/chat` endpoints.
- Optional OpenAI-powered assistant. Without a key, the built-in demo assistant still works.

## Important academic note

This is a working prototype, not a real city deployment. All traffic is synthetic. The adaptive signal controller is a transparent rule-based demonstration, **not a trained reinforcement-learning model**. The charts are heuristic estimates intended for UI demonstration. For a research-grade version, integrate SUMO, collect or choose a suitable traffic dataset, run repeated controlled experiments, and report statistical results.

## Run on Windows using VS Code

1. Install **Python 3.10 or newer** from https://www.python.org/downloads/ and enable **Add Python to PATH** during installation.
2. Extract `UrbanTwin_AI_Project.zip` into a folder you can find, for example `Documents\UrbanTwin`.
3. Open VS Code. Select **File → Open Folder** and choose the extracted `urbantwin` folder.
4. Open **Terminal → New Terminal**.
5. Create a virtual environment:
   ```powershell
   py -m venv .venv
   ```
6. Activate it in PowerShell:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
   If PowerShell blocks activation, use Command Prompt in VS Code and run:
   ```bat
   .venv\Scripts\activate.bat
   ```
7. Install dependencies:
   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
8. Start the website:
   ```powershell
   uvicorn main:app --reload
   ```
9. Open **http://127.0.0.1:8000** in Chrome or Edge. Keep the terminal open while using the site.
10. Check **http://127.0.0.1:8000/api/health** to verify the backend is running.

## Enable LLM chat (optional)

The simulator works without an API key. To enable model-powered chat:

1. Copy `.env.example` to a new file named `.env` in the project root.
2. Put your API key in `.env`:
   ```env
   OPENAI_API_KEY=your_api_key_here
   OPENAI_MODEL=gpt-4o-mini
   ```
3. Stop and restart Uvicorn. Never commit or share `.env`, and do not place the key in browser JavaScript.

LLM calls require internet access and may incur API charges. If the key is absent, the assistant uses a built-in offline response set.

## Project structure

```text
urbantwin/
├── main.py                 # FastAPI backend and optional LLM endpoint
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── templates/
│   └── index.html          # Dashboard structure
└── static/
    ├── style.css           # Responsive UI styles
    └── app.js              # Canvas simulation and UI logic
```

## Suggested extensions for the final MCA submission

1. **SUMO integration:** generate a road network and traffic demand, run fixed-time and adaptive signal programs, and import measured outputs.
2. **Traffic prediction:** train and compare a persistence baseline with Random Forest/XGBoost using a chronological train/test split.
3. **Reinforcement learning:** implement a Gymnasium-compatible signal-control environment and compare an RL policy with fixed-time control.
4. **Emergency route optimization:** use Dijkstra/A* on a road graph and measure route travel time and effects on other traffic.
5. **Reproducible evaluation:** add seeded scenarios, repeated runs, CSV export, mean/standard deviation, and confidence intervals.
6. **Data persistence:** save scenarios and experiment results in SQLite/PostgreSQL.

## Troubleshooting

- `py` is not recognized: reinstall Python and enable PATH, or use `python` instead of `py`.
- `uvicorn` is not recognized: activate `.venv` and run `python -m pip install -r requirements.txt`.
- Page does not load: make sure the terminal shows Uvicorn running and open `http://127.0.0.1:8000` (not the HTML file directly).
- LLM chat says it cannot reach the backend: restart the server and use the URL above.
- LLM provider error: verify the API key, account access, model name, and internet connection. The simulator remains usable without LLM access.
