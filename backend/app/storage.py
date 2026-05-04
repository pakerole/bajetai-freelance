import os
import aiosqlite
from typing import Optional
from datetime import datetime

DB_PATH = os.environ.get("BAJETAI_DB_PATH", "/home/pakerole/bajetai-freelance/backend/data/submissions.db")


async def get_db():
    return aiosqlite.connect(DB_PATH)


async def init_db():
    """Create the submissions table if it doesn't exist."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                company TEXT,
                inquiry_type TEXT NOT NULL,
                description TEXT NOT NULL,
                filename TEXT,
                filepath TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()


async def save_submission(
    name: str,
    email: str,
    inquiry_type: str,
    description: str,
    company: Optional[str] = None,
    filename: Optional[str] = None,
    filepath: Optional[str] = None,
) -> int:
    """Insert a new submission and return its ID."""
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            """
            INSERT INTO submissions (name, email, company, inquiry_type, description, filename, filepath)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (name, email, company, inquiry_type, description, filename, filepath),
        )
        await db.commit()
        return cursor.lastrowid


async def get_submission(submission_id: int):
    """Get a single submission by ID."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT id, name, email, company, inquiry_type, description, filename, filepath, created_at "
            "FROM submissions WHERE id = ?",
            (submission_id,),
        )
        row = await cursor.fetchone()
        if row:
            return dict(row)
        return None


async def list_submissions(limit: int = 100):
    """Return all submissions, most recent first."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT id, name, email, company, inquiry_type, description, filename, filepath, created_at "
            "FROM submissions ORDER BY id DESC LIMIT ?",
            (limit,),
        )
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]
