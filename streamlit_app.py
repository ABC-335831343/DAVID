import streamlit as st
import os

# -----------------------
# הגדרות
# -----------------------
st.set_page_config(page_title="🎧 נגן סיפורים", layout="wide")

ROOT_DIR = os.path.abspath(".")

# -----------------------
# מצב
# -----------------------
if "path" not in st.session_state:
    st.session_state.path = ROOT_DIR

if "search" not in st.session_state:
    st.session_state.search = ""


def go_to(path):
    st.session_state.path = path


def go_back():
    parent = os.path.dirname(st.session_state.path)
    if os.path.exists(parent):
        st.session_state.path = parent


def refresh():
    # טריק פשוט לריענון מלא
    st.rerun()


# -----------------------
# עיצוב
# -----------------------
st.markdown("""
    <style>
        .title {
            font-size: 34px;
            font-weight: 700;
        }
        .card {
            padding: 12px;
            border-radius: 12px;
            border: 1px solid #ddd;
            margin-bottom: 10px;
            background-color: #fafafa;
        }
        .folder {
            color: #1f77b4;
            font-weight: 600;
        }
        .file {
            color: #444;
        }
    </style>
""", unsafe_allow_html=True)

# -----------------------
# כותרת
# -----------------------
st.markdown('<div class="title">🎧 נגן סיפורים</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([2, 5, 1])

with col1:
    if st.button("⬅️ אחורה"):
        go_back()

with col2:
    st.session_state.search = st.text_input("🔍 חיפוש סיפורים או תיקיות", value=st.session_state.search)

with col3:
    if st.button("🔄 רענן"):
        refresh()

st.caption(f"📁 נתיב: {st.session_state.path}")

# -----------------------
# קריאת תיקייה
# -----------------------
current_path = st.session_state.path

try:
    items = sorted(os.listdir(current_path))
except Exception as e:
    st.error(f"שגיאה: {e}")
    st.stop()

folders = []
mp3_files = []

for item in items:
    full_path = os.path.join(current_path, item)

    if os.path.isdir(full_path):
        folders.append(item)
    elif item.lower().endswith(".mp3"):
        mp3_files.append(item)

# פילטר חיפוש
query = st.session_state.search.lower().strip()

if query:
    folders = [f for f in folders if query in f.lower()]
    mp3_files = [f for f in mp3_files if query in f.lower()]

# -----------------------
# תיקיות
# -----------------------
st.subheader("📁 תיקיות")

if folders:
    for folder in folders:
        folder_path = os.path.join(current_path, folder)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        colA, colB = st.columns([6, 1])

        with colA:
            st.markdown(f"📂 <span class='folder'>{folder}</span>", unsafe_allow_html=True)

        with colB:
            if st.button("פתח ▶️", key=folder_path):
                go_to(folder_path)
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("אין תיקיות")

# -----------------------
# קבצי MP3
# -----------------------
st.subheader("🎵 קבצי שמע")

if mp3_files:
    for file in mp3_files:
        file_path = os.path.join(current_path, file)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f"🎧 <span class='file'>{file}</span>", unsafe_allow_html=True)
        st.audio(file_path)
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("אין קבצי MP3")
