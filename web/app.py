from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from web.routes.api import router as api_router, set_engine
from web.routes.websocket import ws_manager

app = FastAPI(title="GhostTrace", version="2.0.0")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

base_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=str(base_dir / "static")), name="static")
app.include_router(api_router, prefix="/api/v1")

try:
    from core.ghost_engine import GhostEngine, GhostConfig
    config = GhostConfig.from_yaml("config/settings.yaml")
    engine = GhostEngine(config)
    set_engine(engine)
except Exception:
    pass


@app.get("/", response_class=HTMLResponse)
async def dashboard():
    return (base_dir / "templates" / "index.html").read_text(encoding="utf-8")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await ws_manager.handle_message(websocket, data)
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)