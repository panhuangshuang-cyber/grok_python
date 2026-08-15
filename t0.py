# read_kdocs_sheet.py
import requests
import pandas as pd
import json
import time
from pathlib import Path

APP_ID   = "AK20260721HSUCGG"
APP_KEY  = "049b4dec0139bc04ba10ecfe776cbe9d"
AUTH_HOST = "https://openapi.wps.cn"

FILE_ID    = "cp0vRakMupN8"    # 来自 kdocs.cn 分享链接的 sid
SHEET_NAME = "工作表1"

TOKEN_CACHE = Path(__file__).resolve().parent / "token.json"

def get_app_token():
    if TOKEN_CACHE.exists():
        try:
            d = json.loads(TOKEN_CACHE.read_text(encoding="utf-8"))
            if d.get("expires_at", 0) > time.time() + 60:
                return d["access_token"]
        except Exception:
            pass

    r = requests.post(
        f"{AUTH_HOST}/oauth2/token",
        data={"grant_type": "client_credentials",
              "client_id": APP_ID, "client_secret": APP_KEY},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=20,
    )
    r.raise_for_status()
    js = r.json()
    tok, exp = js["access_token"], js.get("expires_in", 7199)
    TOKEN_CACHE.write_text(
        json.dumps({"access_token": tok, "expires_at": time.time() + exp},
                   ensure_ascii=False),
        encoding="utf-8",
    )
    return tok

def read_sheet(token):
    headers = {"Authorization": f"Bearer {token}"}

    # 获取 sheet 列表
    r = requests.get(
        f"{AUTH_HOST}/v7/airsheet/{FILE_ID}/worksheets",
        headers=headers, timeout=30,
    )
    r.raise_for_status()
    sheets = (r.json().get("data") or {}).get("sheets") or []

    sheet_id = None
    for s in sheets:
        if s.get("name") == SHEET_NAME:
            sheet_id = s.get("sheet_id")
            break
    if not sheet_id:
        raise RuntimeError(f"未找到工作表: {SHEET_NAME}")

    # 读取单元格
    r = requests.get(
        f"{AUTH_HOST}/v7/airsheet/{FILE_ID}/worksheets/{sheet_id}/range_data"
        f"?range=A1:ZZ500",
        headers=headers, timeout=30,
    )
    r.raise_for_status()
    return (r.json().get("data") or {}).get("range_data") or []

def cells_to_dataframe(cells):
    if not cells:
        return pd.DataFrame()
    last_row = max(c.get("row_from", 0) for c in cells)
    last_col = max(c.get("col_from", 0) for c in cells)
    grid = [["" for _ in range(last_col + 1)] for _ in range(last_row + 1)]
    for c in cells:
        grid[c.get("row_from", 0)][c.get("col_from", 0)] = c.get("cell_text", "")
    if last_row == 0:
        return pd.DataFrame(grid)
    return pd.DataFrame(grid[1:], columns=grid[0])

def main():
    token = get_app_token()
    cells = read_sheet(token)
    df = cells_to_dataframe(cells)

    out_csv = Path(__file__).resolve().parent / "worktable1.csv"
    df.to_csv(out_csv, index=False, encoding="utf-8-sig")
    print(f"✅ {df.shape[0]} 行 × {df.shape[1]} 列 → {out_csv}")

if __name__ == "__main__":
    main()
