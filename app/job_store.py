# app/job_store.py
import sqlite3


def init_db():
    conn = sqlite3.connect("jobs.db")
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS jobs (
                    job_id TEXT PRIMARY KEY,
                    status TEXT,
                    result TEXT
                 )"""
    )
    conn.commit()
    conn.close()


def add_job(job_id):
    conn = sqlite3.connect("jobs.db")
    c = conn.cursor()
    c.execute("INSERT INTO jobs (job_id, status) VALUES (?, ?)", (job_id, "pending"))
    conn.commit()
    conn.close()


def update_job(job_id, result):
    conn = sqlite3.connect("jobs.db")
    c = conn.cursor()
    c.execute(
        "UPDATE jobs SET status = ?, result = ? WHERE job_id = ?",
        ("finished", result, job_id),
    )
    conn.commit()
    conn.close()


def get_job(job_id):
    conn = sqlite3.connect("jobs.db")
    c = conn.cursor()
    c.execute("SELECT status, result FROM jobs WHERE job_id = ?", (job_id,))
    row = c.fetchone()
    conn.close()
    return row
