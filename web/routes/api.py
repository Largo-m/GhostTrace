from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

engine_instance = None
session_manager = None


def set_engine(engine):
    global engine_instance, session_manager
    engine_instance = engine
    if engine:
        session_manager = engine.session


@router.get("/status")
async def get_status():
    if not engine_instance:
        return {
            "engine_running": False,
            "uptime": "0",
            "requests_sent": 0,
            "identities_rotated": 0,
            "active_proxies": 0,
            "message": "Engine offline",
            "timestamp": datetime.now().isoformat()
        }

    return {
        "engine_running": engine_instance._running,
        "uptime": "0",
        "requests_sent": engine_instance._requests_sent,
        "identities_rotated": engine_instance._identities_rotated,
        "active_proxies": engine_instance.proxy_mgr.proxy_count if engine_instance.proxy_mgr else 0,
        "message": "Engine ready",
        "timestamp": datetime.now().isoformat()
    }


@router.post("/rotate")
async def rotate_identity():
    return {
        "success": False,
        "message": "Tor not connected",
        "timestamp": datetime.now().isoformat()
    }


@router.get("/proxies")
async def list_proxies():
    return {"available": [], "count": 0}


@router.get("/chain")
async def get_chain():
    return {"chain": [], "length": 0, "active": False}


@router.post("/test")
async def test_connection():
    return {"message": "Engine not running", "status": "offline"}


@router.post("/scan")
async def run_scan():
    return {"open_ports": [], "message": "Engine offline"}


@router.post("/scrape")
async def scrape_proxies():
    return {"count": 0, "message": "Not implemented"}