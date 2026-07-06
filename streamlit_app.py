import streamlit as st
import os

# -----------------------
# הגדרות עמוד
# -----------------------
st.set_page_config(
    page_title="🎧 נגן סיפורים",
    layout="wide"
)

ROOT_DIR = os.path.abspath(".")

# -----------------------
# מצב אפליקציה
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
    st.rerun()


# -----------------------
# כותרת
# -----------------------
st.title("🎧 נגן סיפורים")

col1, col2, col3 = st.columns([1, 6, 1])

with col1:
    if st.button("⬅️ אחורה"):
        go_back()

with col2:
    st.session_state.search = st.text_input(
        "🔍 חיפוש תיקיות / סיפורים",
        value=st.session_state.search
    )

with col3:
    if st.button("🔄 רענן"):
        refresh()

st.caption(f"📁 נתיב נוכחי: {st.session_state.path}")

# -----------------------
# קריאת תיקייה
# -----------------------
current_path = st.session_state.path

try:
    items = sorted(os.listdir(current_path))
except Exception as e:
    st.error(f"שגיאה בקריאת תיקייה: {e}")
    st.stop()

folders = []
mp3_files = []

for item in items:
    full_path = os.path.join(current_path, item)

    if os.path.isdir(full_path):
        folders.append(item)
    elif item.lower().endswith(".mp3"):
        mp3_files.append(item)

# -----------------------
# חיפוש
# -----------------------
q = st.session_state.search.lower().strip()

if q:
    folders = [f for f in folders if q in f.lower()]
    mp3_files = [f for f in mp3_files if q in f.lower()]

# -----------------------
# תיקיות
# -----------------------
st.subheader("📁 תיקיות")

if folders:
    for folder in folders:
        folder_path = os.path.join(current_path, folder)

        with st.container(border=True):
            colA, colB = st.columns([6, 1])

            with colA:
                st.markdown(f"📂 **{folder}**")

            with colB:
                if st.button("פתח ▶️", key=f"folder_{folder_path}"):
                    go_to(folder_path)
                    st.rerun()
else:
    st.info("אין תיקיות")

# -----------------------
# קבצי MP3
# -----------------------
st.subheader("🎵 קבצי שמע")

if mp3_files:
    for file in mp3_files:
        file_path = os.path.join(current_path, file)

        with st.container(border=True):
            st.markdown(f"🎧 **{file}**")
            st.audio(file_path)
else:
    st.info("אין קבצי MP3 בתיקייה זו")
