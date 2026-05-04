import os
import uuid
import logging

from fastapi import FastAPI, File, Form, HTTPException, UploadFile, Request
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


@app.on_event("startup")
async def startup():
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    await init_db()
    init_telegram(
        bot_token=os.environ.get("TELEGRAM_BOT_TOKEN", ""),
        chat_id=os.environ.get("TELEGRAM_CHAT_ID", ""),
    )
    logger.info("Backend started — DB initialised, upload dir ready")


@app.get("/health")
@app.head("/health")
async def health_root(request: Request):
    if request.method == "HEAD":
        return JSONResponse(content=None, status_code=200)
    return {"status": "ok"}


@app.get("/api/health")
@app.head("/api/health")
async def health_api(request: Request):
    if request.method == "HEAD":
        return JSONResponse(content=None, status_code=200)
    return {"status": "ok"}


@app.post("/api/submit")
async def submit(
    name: str = Form(..., min_length=1),
    email: str = Form(...),
    company: str | None = Form(None),
    inquiry_type: str = Form(..., min_length=1),
    description: str = Form(..., min_length=1),
    file: UploadFile | None = File(None),
):
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
