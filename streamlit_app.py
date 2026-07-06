import streamlit as st
import os

# =========================
# הגדרות בסיס
# =========================
st.set_page_config(
    page_title="🎧 ספריית סיפורים",
    layout="wide"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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
    st.session_state.path = path

def go_back():
    parent = os.path.dirname(st.session_state.path)
    if os.path.exists(parent):
        st.session_state.path = parent

def refresh():
    st.cache_data.clear()
    st.rerun()

# =========================
# UI עליון
# =========================
st.title("🎧 ספריית סיפורים")

col1, col2, col3 = st.columns([1, 6, 1])

with col1:
    st.button("⬅️ חזור", on_click=go_back)

with col2:
    st.session_state.search = st.text_input(
        "🔍 חיפוש סיפורים / תיקיות",
        value=st.session_state.search
    )

with col3:
    st.button("🔄 רענן", on_click=refresh)

st.caption(f"📁 נתיב: {st.session_state.path}")

# =========================
# קריאת תיקייה
# =========================
def load_files(path):
    try:
        items = os.listdir(path)
    except:
        return [], []

    folders = []
    mp3s = []

    for item in sorted(items):
        full = os.path.join(path, item)

        if os.path.isdir(full):
            folders.append(item)
        elif item.lower().endswith(".mp3"):
            mp3s.append(item)

    return folders, mp3s


folders, mp3_files = load_files(st.session_state.path)

# =========================
# חיפוש
# =========================
q = st.session_state.search.lower().strip()

if q:
    folders = [f for f in folders if q in f.lower()]
    mp3_files = [f for f in mp3_files if q in f.lower()]

# =========================
# תיקיות
# =========================
st.subheader("📁 תיקיות")

if not folders:
    st.info("אין תיקיות")
else:
    for folder in folders:
        path = os.path.join(st.session_state.path, folder)

        with st.container(border=True):
            colA, colB = st.columns([5, 1])

            with colA:
                st.markdown(f"📂 **{folder}**")

            with colB:
                st.button(
                    "פתח ▶️",
                    key=f"open_{path}",
                    on_click=set_path,
                    args=(path,)
                )

# =========================
# קבצי MP3
# =========================
st.subheader("🎵 קבצי שמע")

if not mp3_files:
    st.info("אין קבצי MP3")
else:
    for file in mp3_files:
        full = os.path.join(st.session_state.path, file)

        with st.container(border=True):
            st.markdown(f"🎧 **{file}**")
            st.audio(full)
