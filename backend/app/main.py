import os
import time
import uuid
import logging
from collections import defaultdict

import httpx
from fastapi import FastAPI, File, Form, HTTPException, UploadFile, Request, Depends
from fastapi.responses import JSONResponse

from app.models import SubmissionBase
from app.storage import init_db, save_submission, get_submission
from app.telegram import init_telegram, send_submission_notification

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("bajetai")

UPLOAD_DIR = os.environ.get("BAJETAI_UPLOAD_DIR", "/home/pakerole/bajetai-freelance/backend/uploads")

app = FastAPI(title="bajetAI Freelance API", version="0.1.0")

ALLOWED_EXTENSIONS = {".csv", ".xlsx", ".xls", ".json"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

# --- Rate limiter (in-memory, per-IP) ---
RATE_LIMIT = 5          # max requests
RATE_WINDOW = 60        # per 60 seconds
_rate_store: dict[str, list[float]] = defaultdict(list)


def _check_rate_limit(ip: str) -> bool:
    """Return True if IP is within rate limit."""
    now = time.time()
    window = _rate_store[ip]
    # Prune old entries
    _rate_store[ip] = [t for t in window if now - t < RATE_WINDOW]
    if len(_rate_store[ip]) >= RATE_LIMIT:
        return False
    _rate_store[ip].append(now)
    return True


# --- File magic bytes validation ---
FILE_SIGNATURES = {
    b"\x50\x4b\x03\x04": ".xlsx",   # ZIP (xlsx)
    b"\xd0\xcf\x11\xe0": ".xls",    # OLE2 (xls)
}

def _validate_file_content(content: bytes, ext: str) -> bool:
    """Check that file content matches expected type."""
    if ext == ".json":
        # JSON starts with { or [
        return content[:1] in (b"{", b"[", b"\"")
    if ext == ".csv":
        # CSV is text — check it's not binary gibberish
        try:
            content[:512].decode("utf-8")
            return True
        except UnicodeDecodeError:
            return False
    # Binary formats: check magic bytes
    for sig, sig_ext in FILE_SIGNATURES.items():
        if ext == sig_ext and content[:4] == sig:
            return True
    return False


# --- Custom error handler (no stack trace leaks) ---
@app.exception_handler(Exception)
async def generic_error_handler(request: Request, exc: Exception):
    logger.exception("Unhandled error on %s %s", request.method, request.url.path)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


@app.on_event("startup")
async def startup():
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    await init_db()
    init_telegram(
        bot_token=os.environ.get("TELEGRAM_BOT_TOKEN", ""),
        chat_id=os.environ.get("TELEGRAM_CHAT_ID", ""),
    )
    logger.info("Backend started — DB initialised, upload dir ready")


async def _check_health():
    """Check backend + frontend containers."""
    checks = {"backend": "ok", "frontend": "ok"}
    overall = "ok"

    # Check frontend via localhost (same Docker network via host)
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get("http://host.docker.internal:8030/")
            if resp.status_code >= 500:
                checks["frontend"] = f"error: upstream returned {resp.status_code}"
                overall = "degraded"
            elif resp.status_code >= 400:
                # 4xx on GET / is unusual but frontend is alive
                checks["frontend"] = f"warn: {resp.status_code}"
                overall = "degraded"
    except httpx.ConnectError:
        checks["frontend"] = "error: connection refused (container down?)"
        overall = "down"
    except httpx.TimeoutException:
        checks["frontend"] = "error: timeout"
        overall = "degraded"
    except Exception as e:
        checks["frontend"] = f"error: {e}"
        overall = "degraded"

    status_code = 200 if overall == "ok" else (503 if overall == "down" else 200)
    return {
        "status": overall,
        "checks": checks,
    }, status_code


@app.get("/health")
@app.head("/health")
async def health_root(request: Request):
    if request.method == "HEAD":
        return JSONResponse(content=None, status_code=200)
    result, code = await _check_health()
    return JSONResponse(content=result, status_code=code)


@app.get("/api/health")
@app.head("/api/health")
async def health_api(request: Request):
    if request.method == "HEAD":
        return JSONResponse(content=None, status_code=200)
    result, code = await _check_health()
    return JSONResponse(content=result, status_code=code)


@app.post("/api/submit")
async def submit(
    request: Request,
    name: str = Form(..., min_length=1),
    email: str = Form(...),
    company: str | None = Form(None),
    inquiry_type: str = Form(..., min_length=1),
    description: str = Form(..., min_length=1),
    file: UploadFile | None = File(None),
):
    # Rate limit check
    client_ip = request.client.host if request.client else "unknown"
    if not _check_rate_limit(client_ip):
        raise HTTPException(status_code=429, detail="Too many requests. Please try again later.")

    # Validate fields with Pydantic
    try:
        validated = SubmissionBase(
            name=name,
            email=email,
            company=company or None,
            inquiry_type=inquiry_type,
            description=description,
        )
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

    # Handle optional file upload
    saved_filename: str | None = None
    saved_filepath: str | None = None

    if file and file.filename:
        # Validate extension
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"File type '{ext}' not allowed. Accepted: {', '.join(ALLOWED_EXTENSIONS)}",
            )

        # Read content and check size
        content = await file.read()
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="File too large (max 10 MB)")

        # Validate file content matches extension
        if not _validate_file_content(content, ext):
            raise HTTPException(status_code=400, detail="File content doesn't match the declared file type")

        # Save with UUID name
        saved_filename = f"{uuid.uuid4().hex}{ext}"
        saved_filepath = os.path.join(UPLOAD_DIR, saved_filename)
        with open(saved_filepath, "wb") as f:
            f.write(content)
        logger.info("File saved: %s", saved_filepath)

    # Store in SQLite
    submission_id = await save_submission(
        name=validated.name,
        email=validated.email,
        company=validated.company,
        inquiry_type=validated.inquiry_type,
        description=validated.description,
        filename=saved_filename,
        filepath=saved_filepath,
    )
    logger.info("Submission #%d saved from %s <%s>", submission_id, validated.name, validated.email)

    # Send Telegram notification (fire-and-forget, errors are logged but non-blocking)
    send_submission_notification(
        name=validated.name,
        email=validated.email,
        inquiry_type=validated.inquiry_type,
        description=validated.description,
        company=validated.company,
        filename=saved_filename,
    )

    # Fetch full record from DB (includes created_at)
    row = await get_submission(submission_id)

    return row
