"""Чтение данных из Google Sheets и форматирование чисел.

Доступы берутся из Secrets приложения на Streamlit Cloud, а при работе
с компьютера — из локальных файлов. В коде секретов нет.
"""
import json
import re
import urllib.parse
import urllib.request

LOCAL_SECRET = "/opt/data/google_client_secret.json"
LOCAL_TOKEN = "/opt/data/google_token.json"


def _creds():
    """client_id, client_secret, refresh_token либо None."""
    try:
        import streamlit as st
        return (st.secrets["google_client_id"],
                st.secrets["google_client_secret"],
                st.secrets["google_refresh_token"])
    except Exception:
        pass
    try:
        sp = json.load(open(LOCAL_SECRET))["installed"]
        return (sp["client_id"], sp["client_secret"],
                json.load(open(LOCAL_TOKEN))["refresh_token"])
    except Exception:
        return None


def access_token():
    cr = _creds()
    if not cr:
        return None
    data = urllib.parse.urlencode({"client_id": cr[0], "client_secret": cr[1],
                                   "refresh_token": cr[2],
                                   "grant_type": "refresh_token"}).encode()
    req = urllib.request.Request("https://oauth2.googleapis.com/token", data=data)
    return json.loads(urllib.request.urlopen(req, timeout=25).read())["access_token"]


def values(sheet_id, tab, rng="A1:Z200"):
    """Диапазон листа таблицы. Список строк, в каждой строке список ячеек."""
    tok = access_token()
    if not tok:
        return []
    full = urllib.parse.quote(tab + "!" + rng)
    url = ("https://sheets.googleapis.com/v4/spreadsheets/" + sheet_id +
           "/values/" + full + "?majorDimension=ROWS")
    req = urllib.request.Request(url, headers={"Authorization": "Bearer " + tok})
    return json.loads(urllib.request.urlopen(req, timeout=30).read()).get("values", [])


def num(v):
    """Число из ячейки: пробелы, запятые, знак рубля и проценты не мешают."""
    s = str(v).replace(chr(160), "").replace(" ", "").replace(",", ".")
    s = re.sub(r"[^0-9.\-]", "", s)
    try:
        return float(s)
    except ValueError:
        return 0.0


def fmt(v, dash="—"):
    """Деньги: 1 234 567. Нули и пустое показываем прочерком."""
    if abs(v) < 0.5:
        return dash
    out = f"{v:,.0f}".replace(",", " ")
    return dash if out in ("-0", "0") else out


def pct(v):
    """Проценты: 12,5%."""
    return (f"{v:.1f}%").replace(".", ",")


def ci(letter):
    """Номер колонки по букве: C -> 2, AA -> 26."""
    n = 0
    for ch in letter:
        n = n * 26 + (ord(ch) - 64)
    return n - 1


def cl(i):
    """Буква колонки по номеру: 2 -> C, 26 -> AA."""
    s = ""
    i += 1
    while i:
        i, r = divmod(i - 1, 26)
        s = chr(65 + r) + s
    return s
