import streamlit as st

st.title("בדיקה ✅")
st.write("האפליקציה עובדת")

st.success("אם אתה רואה את זה → הכל תקין")
"""
import streamlit as st
import os

# =========================
# הגדרות
# =========================
st.set_page_config(page_title="🎧 סיפורים", layout="wide")

# =========================
# ROOT יציב ל-Streamlit Cloud
# =========================
BASE_DIR = os.getcwd()

# fallback אם משהו נשבר
if not os.path.exists(BASE_DIR):
    BASE_DIR = "."

# =========================
# מצב
# =========================
if "path" not in st.session_state:
    st.session_state.path = BASE_DIR

if "search" not in st.session_state:
    st.session_state.search = ""

# =========================
# פונקציות
# =========================
def set_path(path):
    if os.path.exists(path):
        st.session_state.path = path

def back():
    parent = os.path.dirname(st.session_state.path)
    if os.path.exists(parent):
        st.session_state.path = parent

def reload():
    st.rerun()

# =========================
# UI
# =========================
st.title("🎧 ספריית סיפורים")

c1, c2, c3 = st.columns([1, 6, 1])

with c1:
    st.button("⬅️ אחורה", on_click=back)

with c2:
    st.session_state.search = st.text_input(
        "🔍 חיפוש",
        value=st.session_state.search
    )

with c3:
    st.button("🔄 רענן", on_click=reload)

st.caption(f"📁 {st.session_state.path}")

current = st.session_state.path

# =========================
# קריאה בטוחה
# =========================
try:
    items = os.listdir(current)
except Exception as e:
    st.error(f"שגיאה בטעינת תיקייה: {e}")
    st.stop()

folders = []
mp3s = []

for i in sorted(items):
    full = os.path.join(current, i)

    try:
        if os.path.isdir(full):
            folders.append(i)
        elif i.lower().endswith(".mp3"):
            mp3s.append(i)
    except:
        continue

# =========================
# חיפוש
# =========================
q = st.session_state.search.lower().strip()

if q:
    folders = [f for f in folders if q in f.lower()]
    mp3s = [f for f in mp3s if q in f.lower()]

# =========================
# תיקיות
# =========================
st.subheader("📁 תיקיות")

if folders:
    for f in folders:
        path = os.path.join(current, f)

        with st.container(border=True):
            col1, col2 = st.columns([6, 1])

            with col1:
                st.write("📂", f)

            with col2:
                st.button("פתח", key=path, on_click=set_path, args=(path,))
else:
    st.info("אין תיקיות")

# =========================
# MP3
# =========================
st.subheader("🎵 קבצי שמע")

if mp3s:
    for m in mp3s:
        full = os.path.join(current, m)

        with st.container(border=True):
            st.write("🎧", m)
            st.audio(full)
else:
    st.info("אין קבצי MP3")
"""
