import os
import re
import sqlite3
import shutil
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict

# =====================================================
# 設定
# =====================================================
CABINET_DB = r"cb5\data\cabinet.odbx"
OFFICE_DB  = r"cb5\data\office.odbx"
FILE_BASE  = r"cb5\file\Cabinet"
OUTPUT_DIR = r"root"
LOG_FILE   = "Restoration.csv"

MAX_WORKERS = 8   # SSD: 8 / HDD: 4
INVALID_CHARS = r'[\\/:*?"<>|]'

# =====================================================
# ユーティリティ
# =====================================================
def sanitize(name: str) -> str:
    return re.sub(INVALID_CHARS, "_", name)

def le_hex_to_int(hex8: str) -> int:
    return int(hex8[6:8] + hex8[4:6] + hex8[2:4] + hex8[0:2], 16)

# =====================================================
# DB 全件ロード
# =====================================================
def load_db(path):
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute("SELECT oid, hex(object_data) FROM cb_main")
    data = {oid: hexdata for oid, hexdata in cur.fetchall()}
    conn.close()
    return data

print("DBロード中...")
cabinet_map = load_db(CABINET_DB)
office_map  = load_db(OFFICE_DB)
print(f"Cabinet 件数 = {len(cabinet_map)}")
