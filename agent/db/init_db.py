"""
Initialize submission_log.db — single source of truth for all application state.
Run once: python init_db.py
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "submission_log.db"


def init():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
    CREATE TABLE IF NOT EXISTS applications (
        id                      INTEGER PRIMARY KEY AUTOINCREMENT,
        app_id                  TEXT UNIQUE,          -- e.g. APP-001
        role                    TEXT NOT NULL,
        company                 TEXT NOT NULL,
        location                TEXT,
        region                  TEXT,
        url                     TEXT,
        match_score             INTEGER,
        compensation            TEXT,
        priority                TEXT DEFAULT 'medium',
        status                  TEXT DEFAULT 'shortlisted',
        jd_summary              TEXT,
        gap_keywords            TEXT,                 -- JSON array as string
        cover_letter_text       TEXT,
        submitted               INTEGER DEFAULT 0,
        submitted_at            TEXT,
        follow_up_drafted       INTEGER DEFAULT 0,
        follow_up_drafted_at    TEXT,
        follow_up_connection_note TEXT,
        follow_up_inmail        TEXT,
        follow_up_sent          INTEGER DEFAULT 0,
        follow_up_sent_at       TEXT,
        hiring_manager_name     TEXT,
        hiring_manager_linkedin TEXT,
        company_insight         TEXT,
        notes                   TEXT,
        created_at              TEXT DEFAULT (datetime('now')),
        updated_at              TEXT DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS approval_events (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        application_id  INTEGER REFERENCES applications(id),
        event_type      TEXT,   -- 'cover_letter_approved', 'submission_approved', 'follow_up_approved'
        approved        INTEGER DEFAULT 0,
        approved_at     TEXT,
        rejected_reason TEXT
    );

    CREATE TABLE IF NOT EXISTS scrape_log (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        query       TEXT,
        location    TEXT,
        platform    TEXT,
        results_n   INTEGER,
        scraped_at  TEXT DEFAULT (datetime('now'))
    );
    """)

    conn.commit()
    conn.close()
    print(f"✅ Database initialised: {DB_PATH}")


if __name__ == "__main__":
    init()
