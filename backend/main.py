from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from pydantic import BaseModel
import os

from .database import init_db
from .auth.router import router as auth_router
from .ride.router import router as ride_router
from .ocr import parse_cr_text


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="PythonLogin — Multi-App Auth Service",
    description="Reusable authentication framework with facial registration",
    version="1.0.0",
    lifespan=lifespan,
)

# Global exception handler for debugging 500 errors
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    import traceback
    err_trace = traceback.format_exc()
    print(f"CRITICAL ERROR:\n{err_trace}")
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal Server Error",
            "error": str(exc),
            "trace": err_trace
        },
        headers={
            "Access-Control-Allow-Origin": request.headers.get("origin") or "*",
            "Access-Control-Allow-Credentials": "true"
        }
    )

# CORS configuration - Allow local dev, LAN IP, mobile webviews (Capacitor/Cordova), and cloud deployments
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r".*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve stored face images statically with CORS support
FACE_DIR = os.path.join(os.path.dirname(__file__), "face_images")
os.makedirs(FACE_DIR, exist_ok=True)

DRIVER_DIR = os.path.join(os.path.dirname(__file__), "driver_docs")
os.makedirs(DRIVER_DIR, exist_ok=True)

class CORSStaticFiles(StaticFiles):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def __call__(self, scope, receive, send):
        # We need headers here to get origin
        headers = dict(scope.get("headers", []))
        async def send_with_cors(message):
            if message["type"] == "http.response.start":
                # Find headers
                msg_headers = dict(message.get("headers", []))
                origin = headers.get(b"origin", b"*").decode()
                msg_headers[b"access-control-allow-origin"] = origin.encode()
                msg_headers[b"access-control-allow-credentials"] = b"true"
                message["headers"] = list(msg_headers.items())
            await send(message)
        await super().__call__(scope, receive, send_with_cors)

app.mount("/face_images", CORSStaticFiles(directory=FACE_DIR), name="face_images")
app.mount("/driver_docs", CORSStaticFiles(directory=DRIVER_DIR), name="driver_docs")

app.include_router(auth_router)
app.include_router(ride_router)


# ── OCR document reader (EasyOCR) ──────────────────────────────
_EASYOCR_READER = None


def _get_easyocr_reader():
    global _EASYOCR_READER
    if _EASYOCR_READER is None:
        import easyocr
        _EASYOCR_READER = easyocr.Reader(["en"], gpu=False, verbose=False)
    return _EASYOCR_READER


def _run_easyocr(arr):
    return [(box, text, conf) for box, text, conf in _get_easyocr_reader().readtext(arr)]


class OcrRequest(BaseModel):
    dataUrl: str  # base64 image data URL


@app.post("/api/ocr/{engine}")
def ocr_document(engine: str, payload: OcrRequest):
    engine = (engine or "").lower()
    if engine not in ("easyocr", "parse_cr"):
        return JSONResponse({"ok": False, "error": f"unknown OCR engine '{engine}'"}, status_code=400)

    data_url = payload.dataUrl or ""
    if "base64," not in data_url:
        return JSONResponse({"ok": False, "error": "expected a base64 image data URL"}, status_code=400)
    import base64 as _b64
    try:
        raw = _b64.b64decode(data_url.split("base64,", 1)[1])
    except Exception as e:
        return JSONResponse({"ok": False, "error": f"bad base64: {e}"}, status_code=400)

    try:
        import io
        import numpy as np
        from PIL import Image
        img = Image.open(io.BytesIO(raw)).convert("RGB")
        arr = np.array(img)
        results = _run_easyocr(arr)
    except ModuleNotFoundError as e:
        pkg = "easyocr"
        return JSONResponse(
            {"ok": False, "error": f"{engine} not installed ({e}). Run: pip install {pkg}"},
            status_code=500)
    except Exception as e:
        return JSONResponse({"ok": False, "error": f"OCR failed: {e}"}, status_code=500)

    words = []
    for box, text, conf in results:
        t = (text or "").strip()
        if not t:
            continue
        xs = [float(p[0]) for p in box]
        ys = [float(p[1]) for p in box]
        words.append({
            "text": t,
            "x0": min(xs), "x1": max(xs), "y0": min(ys), "y1": max(ys),
            "conf": float(conf),
        })

    # Support CR parsing via /api/ocr/parse_cr even when this dynamic route matches first.
    if engine == "parse_cr":
        raw_text = "\n".join([w["text"] for w in words if w.get("text")])
        parsed = parse_cr_text(raw_text)
        return {"ok": True, "engine": engine, "text": raw_text, "parsed": parsed}

    return {"ok": True, "engine": engine, "words": words,
            "width": img.width, "height": img.height, "count": len(words)}



@app.get("/")
async def root():
    return {
        "service": "CaelRide Backend API",
        "docs": "/docs",
        "status": "online",
        "health": "/auth/health",
    }






