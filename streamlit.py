import streamlit as st
import json
import pandas as pd
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Ramadan Prayer Timetable (IST)",
    page_icon="🌙",
    layout="wide"
)

# ---------------- LOAD DATA ----------------
with open("enhanced_ramadan.json", "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)
df["Ramadan Day"] = df["Ramadan Day"].astype(int)

# ---------------- TIME CONVERSION ----------------
IST_OFFSET = 5 * 60 + 30  # 5 hours 30 minutes


def utc_to_ist(time_str):
    if not time_str:
        return ""
    h, m = map(int, time_str.split(":"))
    total = h * 60 + m + IST_OFFSET
    total %= 24 * 60
    return f"{total // 60:02d}:{total % 60:02d}"


TIME_COLUMNS = [
    "Sehri Ends", "Iftar Time",
    "Fajr", "Sunrise", "Dhuhr",
    "Asr", "Maghrib", "Isha"
]

for col in TIME_COLUMNS:
    df[col] = df[col].apply(utc_to_ist)

# ---------------- UI ----------------
st.title("🌙 Ramadan Prayer Timetable (IST)")
st.caption("🇮🇳 Times shown in Indian Standard Time (UTC + 5:30)")

search_input = st.text_input(
    "🔍 Search by Gregorian date (DD-MM-YYYY) or Ramadan day",
    placeholder="e.g. 18-02-2026 or 5"
)

filtered_df = df.copy()

if search_input:
    filtered_df = df[df["Gregorian Date"] == search_input]

    if filtered_df.empty and search_input.isdigit():
        filtered_df = df[df["Ramadan Day"] == int(search_input)]

# ---------------- HIGHLIGHT TODAY ----------------
today_ist = (datetime.utcnow().timestamp() + 19800)
today_str = datetime.utcfromtimestamp(today_ist).strftime("%d-%m-%Y")


def highlight_today(row):
    if row["Gregorian Date"] == today_str:
        return ["background-color: #065f46; color: white"] * len(row)
    return [""] * len(row)

# ---------------- DISPLAY ----------------
st.subheader("📅 Full Ramadan Prayer Timings")

display_columns = [
    "Gregorian Date",
    "Weekday",
    "Hijri Date",
    "Ramadan Day",
    "Sehri Ends",
    "Iftar Time",
    "Fast Duration",
    "Fajr",
    "Sunrise",
    "Dhuhr",
    "Asr",
    "Maghrib",
    "Isha"
]

st.dataframe(
    filtered_df[display_columns].style.apply(highlight_today, axis=1),
    use_container_width=True,
    hide_index=True
)

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("🕌 Times are converted from UTC to IST • Moon sighting may vary")
