import os
import sqlite3
import json
from typing import Any, Dict, List, Optional, Tuple

DB_PATH = os.path.join(os.path.dirname(__file__), "directory.db")

CATEGORIES = [
    "Tank Suppliers",
    "Filter & Pipe Vendors",
    "Certified Plumbers",
    "Installation Services",
]


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS vendors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            business_name TEXT NOT NULL,
            logo_url TEXT,
            category TEXT NOT NULL,
            contact_person TEXT,
            phone TEXT,
            email TEXT,
            address TEXT,
            city TEXT,
            pincode TEXT,
            lat REAL,
            lng REAL,
            description TEXT,
            gallery_urls TEXT,
            rating_avg REAL DEFAULT 0,
            rating_count INTEGER DEFAULT 0,
            status TEXT DEFAULT 'pending',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vendor_id INTEGER NOT NULL,
            rating INTEGER NOT NULL,
            comment TEXT,
            user_name TEXT,
            status TEXT DEFAULT 'pending',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(vendor_id) REFERENCES vendors(id) ON DELETE CASCADE
        )
        """
    )

    cur.execute("CREATE INDEX IF NOT EXISTS idx_vendors_city ON vendors(city)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_vendors_pincode ON vendors(pincode)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_vendors_status ON vendors(status)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_vendors_category ON vendors(category)")

    cur.execute("CREATE INDEX IF NOT EXISTS idx_reviews_status ON reviews(status)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_reviews_vendor ON reviews(vendor_id)")

    conn.commit()
    conn.close()


# Utility

def _row_to_dict(row: sqlite3.Row) -> Dict[str, Any]:
    return {k: row[k] for k in row.keys()}


# Vendors

def add_vendor(data: Dict[str, Any]) -> int:
    conn = get_conn()
    cur = conn.cursor()
    fields = [
        "business_name",
        "logo_url",
        "category",
        "contact_person",
        "phone",
        "email",
        "address",
        "city",
        "pincode",
        "lat",
        "lng",
        "description",
        "gallery_urls",
        "status",
    ]
    values = [data.get(f) for f in fields]
    cur.execute(
        f"INSERT INTO vendors ({', '.join(fields)}) VALUES ({', '.join(['?']*len(fields))})",
        values,
    )
    vid = cur.lastrowid
    conn.commit()
    conn.close()
    return vid


def submit_vendor_submission(data: Dict[str, Any]) -> int:
    data = data.copy()
    data["status"] = data.get("status") or "pending"
    if data.get("gallery_urls") and not isinstance(data["gallery_urls"], str):
        data["gallery_urls"] = json.dumps(data["gallery_urls"])  # ensure string
    return add_vendor(data)


def update_vendor(vendor_id: int, data: Dict[str, Any]) -> None:
    if not data:
        return
    conn = get_conn()
    cur = conn.cursor()
    sets = []
    values: List[Any] = []
    for k, v in data.items():
        sets.append(f"{k} = ?")
        values.append(v)
    sets.append("updated_at = CURRENT_TIMESTAMP")
    sql = f"UPDATE vendors SET {', '.join(sets)} WHERE id = ?"
    values.append(vendor_id)
    cur.execute(sql, values)
    conn.commit()
    conn.close()


def delete_vendor(vendor_id: int) -> None:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM vendors WHERE id = ?", (vendor_id,))
    conn.commit()
    conn.close()


def get_vendor(vendor_id: int) -> Optional[Dict[str, Any]]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM vendors WHERE id = ?", (vendor_id,))
    row = cur.fetchone()
    conn.close()
    return _row_to_dict(row) if row else None


def list_vendors(
    city_query: Optional[str] = None,
    pincode: Optional[str] = None,
    category: Optional[str] = None,
    only_approved: bool = True,
    limit: int = 200,
) -> List[Dict[str, Any]]:
    conn = get_conn()
    cur = conn.cursor()

    where = []
    params: List[Any] = []
    if only_approved:
        where.append("status = 'approved'")
    if category and category != "All":
        where.append("category = ?")
        params.append(category)
    if pincode:
        where.append("pincode = ?")
        params.append(str(pincode))
    if city_query:
        where.append("LOWER(city) LIKE ?")
        params.append(f"%{city_query.lower()}%")

    where_sql = f"WHERE {' AND '.join(where)}" if where else ""
    sql = f"SELECT * FROM vendors {where_sql} ORDER BY rating_avg DESC, business_name ASC LIMIT ?"
    params.append(limit)

    cur.execute(sql, params)
    rows = cur.fetchall()
    conn.close()
    return [_row_to_dict(r) for r in rows]


def list_pending_vendors(limit: int = 200) -> List[Dict[str, Any]]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM vendors WHERE status = 'pending' ORDER BY created_at ASC LIMIT ?",
        (limit,),
    )
    rows = cur.fetchall()
    conn.close()
    return [_row_to_dict(r) for r in rows]


def approve_vendor(vendor_id: int) -> None:
    update_vendor(vendor_id, {"status": "approved"})


def reject_vendor(vendor_id: int) -> None:
    update_vendor(vendor_id, {"status": "rejected"})


# Reviews

def add_review(vendor_id: int, rating: int, comment: str, user_name: Optional[str]) -> int:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO reviews (vendor_id, rating, comment, user_name, status) VALUES (?, ?, ?, ?, 'pending')",
        (vendor_id, rating, comment, user_name),
    )
    rid = cur.lastrowid
    conn.commit()
    conn.close()
    return rid


def list_reviews(vendor_id: int, only_approved: bool = True) -> List[Dict[str, Any]]:
    conn = get_conn()
    cur = conn.cursor()
    if only_approved:
        cur.execute(
            "SELECT * FROM reviews WHERE vendor_id = ? AND status = 'approved' ORDER BY created_at DESC",
            (vendor_id,),
        )
    else:
        cur.execute(
            "SELECT * FROM reviews WHERE vendor_id = ? ORDER BY created_at DESC",
            (vendor_id,),
        )
    rows = cur.fetchall()
    conn.close()
    return [_row_to_dict(r) for r in rows]


def list_pending_reviews(limit: int = 200) -> List[Dict[str, Any]]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT r.*, v.business_name FROM reviews r JOIN vendors v ON r.vendor_id = v.id WHERE r.status = 'pending' ORDER BY r.created_at ASC LIMIT ?",
        (limit,),
    )
    rows = cur.fetchall()
    conn.close()
    return [_row_to_dict(r) for r in rows]


def _recalc_vendor_rating(vendor_id: int) -> None:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT COUNT(*) as cnt, AVG(rating) as avg_rating FROM reviews WHERE vendor_id = ? AND status = 'approved'",
        (vendor_id,),
    )
    row = cur.fetchone()
    cnt = int(row["cnt"]) if row and row["cnt"] is not None else 0
    avg_rating = float(row["avg_rating"]) if row and row["avg_rating"] is not None else 0.0
    cur.execute(
        "UPDATE vendors SET rating_avg = ?, rating_count = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (avg_rating, cnt, vendor_id),
    )
    conn.commit()
    conn.close()


def approve_review(review_id: int) -> None:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE reviews SET status = 'approved' WHERE id = ?", (review_id,))
    cur.execute("SELECT vendor_id FROM reviews WHERE id = ?", (review_id,))
    row = cur.fetchone()
    conn.commit()
    conn.close()
    if row:
        _recalc_vendor_rating(int(row["vendor_id"]))


def reject_review(review_id: int) -> None:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM reviews WHERE id = ?", (review_id,))
    conn.commit()
    conn.close()


# Ensure DB exists at import
init_db()
