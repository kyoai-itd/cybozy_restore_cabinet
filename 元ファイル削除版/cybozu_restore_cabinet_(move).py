import sqlite3
import re
import shutil
import csv
from pathlib import Path

# ===== 設定 =====
CABINET_DB = "cb5/data/cabinet.odbx"
OFFICE_DB  = "cb5/data/office.odbx"
FILE_SRC   = Path("cb5/file/Cabinet")
BASE_OUT   = Path("root")
LOG_FILE   = "Restoration.csv"

# ===== グローバル =====
folder_map = {}        # OID -> Path
children_map = {}      # ParentOID -> [ChildOID]
folder_names = {}      # OID -> FolderName
used_names = set()     # (dir, filename)
audit_rows = []

