"""
Seed submission_log.db with the 5 shortlisted applications.
Run once: python db/seed.py
"""
import sqlite3, json
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent / "submission_log.db"

APPS = [
    {
        "app_id": "APP-001",
        "role": "AI Architect",
        "company": "Datacom Connect",
        "location": "Brisbane, QLD, Australia",
        "region": "australia",
        "url": "https://to.indeed.com/aapxg2fzcqx7",
        "match_score": 78,
        "compensation": "AUD $100,000 - $140,000",
        "priority": "high",
        "status": "shortlisted",
        "gap_keywords": json.dumps(["solution architecture", "enterprise AI strategy", "cloud architecture patterns"]),
        "notes": "Strongest CV match. RAG + Azure OpenAI + governance align well.",
    },
    {
        "app_id": "APP-002",
        "role": "Chief Technical Officer",
        "company": "Jar Pay Trading Limited",
        "location": "London, UK",
        "region": "uk",
        "url": "https://to.indeed.com/aand6f2fj2rz",
        "match_score": 71,
        "compensation": "£100,000 - £120,000",
        "priority": "high",
        "status": "shortlisted",
        "gap_keywords": json.dumps(["payment rails", "technical roadmap ownership", "fintech compliance"]),
        "notes": "Blockchain Architect cert + AI strategy = strong CTO narrative.",
    },
    {
        "app_id": "APP-003",
        "role": "Lead Security Engineer (AI/DeFi)",
        "company": "Binance",
        "location": "Brisbane, QLD, Australia",
        "region": "australia",
        "url": "https://to.indeed.com/aammt6x4sppy",
        "match_score": 62,
        "compensation": "AUD $85,000 - $135,000",
        "priority": "medium",
        "status": "shortlisted",
        "gap_keywords": json.dumps(["DeFi protocol security", "smart contract auditing", "zero-knowledge proofs"]),
        "notes": "Blockchain cert relevant. DeFi security gap.",
    },
    {
        "app_id": "APP-004",
        "role": "Head of AI Engineering",
        "company": "CellIQ",
        "location": "Mayfair, London, UK",
        "region": "uk",
        "url": "https://to.indeed.com/aa897xpmnbsn",
        "match_score": 70,
        "compensation": "£29,619 - £135,009",
        "priority": "medium",
        "status": "review",
        "gap_keywords": json.dumps([]),
        "notes": "Listed part-time — confirm if full-time track available.",
    },
    {
        "app_id": "APP-005",
        "role": "Generative AI Lead",
        "company": "GBS UK",
        "location": "London, UK",
        "region": "uk",
        "url": "https://to.indeed.com/aah2q6xk6yyk",
        "match_score": 74,
        "compensation": "£50,000 - £75,000",
        "priority": "medium",
        "status": "review",
        "gap_keywords": json.dumps([]),
        "notes": "Comp below market. Strong GenAI technical match.",
    },
]

conn = sqlite3.connect(DB_PATH)
for a in APPS:
    conn.execute("""
        INSERT OR IGNORE INTO applications
          (app_id, role, company, location, region, url, match_score,
           compensation, priority, status, gap_keywords, notes, created_at, updated_at)
        VALUES
          (:app_id,:role,:company,:location,:region,:url,:match_score,
           :compensation,:priority,:status,:gap_keywords,:notes,
           datetime('now'), datetime('now'))
    """, a)
conn.commit()
conn.close()
print(f"✅ Seeded {len(APPS)} applications into submission_log.db")
