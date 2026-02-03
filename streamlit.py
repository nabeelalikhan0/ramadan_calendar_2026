import streamlit as st
import json
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Ramadan Prayer Timetable",
    page_icon="🌙",
    layout="wide"
)

# ---------------- LOAD DATA ----------------
with open("clean_ramadan.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Convert to DataFrame
rows = []
for d in data:
    row = {
        "Gregorian Date": d["gregorian_date"],
        "Weekday": d["weekday"],
        "Hijri Date": d["hijri_date"],
        "Ramadan Day": int(d["ramadan_day"]),
        **d["prayers"]
    }
    rows.append(row)

df = pd.DataFrame(rows)

# ---------------- UI ----------------
st.title("🌙 Ramadan Prayer Timetable")
st.caption("Location based on fixed coordinates • Clean & easy to read")

# Search by date
search_date = st.text_input(
    "🔍 Enter Ramadan Day or Search by Gregorian date (DD-MM-YYYY)",
    placeholder="e.g. 18-02-2026"
)

filtered_df = df
if search_date:
    filtered_df = df[df["Gregorian Date"] == search_date]
    if filtered_df.empty:
        try:
            filtered_df = df[df["Ramadan Day"] == int(search_date)]
        except ValueError:
            filtered_df = df[df["Ramadan Day"] == 0]  # Return empty if not a valid day number

# Highlight today (optional)
today_str = datetime.utcnow().strftime("%d-%m-%Y")

def highlight_today(row):
    if row["Gregorian Date"] == today_str:
        return ["background-color: #1f2937; color: white"] * len(row)
    return [""] * len(row)

st.subheader("📅 Full Month Timings")

st.dataframe(
    filtered_df.style.apply(highlight_today, axis=1),
    use_container_width=True,
    hide_index=True
)

# Footer
st.markdown("---")
st.caption("🕌 Times shown are calculated automatically • Moon sighting may vary")
