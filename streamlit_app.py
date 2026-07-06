import streamlit as st
import os

st.set_page_config(page_title="🎧 סיפורים", layout="wide")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ======================
# STATE בסיסי בלבד
# ======================
if "path" not in st.session_state:
    st.session_state.path = BASE_DIR

if "search" not in st.session_state:
    st.session_state.search = ""

if "current_file" not in st.session_state:
    st.session_state.current_file = None


# ======================
# כותרת
# ======================
st.title("🎧 ספריית סיפורים")

# ======================
# ניווט
# ======================
col1, col2 = st.columns([1, 5])

with col1:
    if st.button("⬅️ חזור"):
        parent = os.path.dirname(st.session_state.path)
        if os.path.exists(parent):
            st.session_state.path = parent
            st.session_state.current_file = None

with col2:
    st.session_state.search = st.text_input("🔍 חיפוש", st.session_state.search)

st.divider()

current_path = st.session_state.path

# ======================
# קריאת קבצים
# ======================
try:
    items = os.listdir(current_path)
except:
    st.error("שגיאה בקריאת תיקייה")
    st.stop()

folders = []
mp3s = []

for item in sorted(items):
    full = os.path.join(current_path, item)

    if os.path.isdir(full):
        folders.append((item, full))
    elif item.lower().endswith(".mp3"):
        mp3s.append((item, full))

# ======================
# חיפוש
# ======================
q = st.session_state.search.lower().strip()

if q:
    folders = [(n,p) for n,p in folders if q in n.lower()]
    mp3s = [(n,p) for n,p in mp3s if q in n.lower()]

# ======================
# תיקיות
# ======================
st.subheader("📁 תיקיות")

if not folders:
    st.write("אין תיקיות")
else:
    for name, path in folders:
        col1, col2 = st.columns([6,1])

        with col1:
            st.write("📂", name)

        with col2:
            if st.button("פתח", key=path):
                st.session_state.path = path
                st.session_state.current_file = None

st.divider()

# ======================
# קבצים
# ======================
st.subheader("🎵 קבצי MP3")

if not mp3s:
    st.write("אין קבצים")
else:
    for name, path in mp3s:
        col1, col2 = st.columns([6,1])

        with col1:
            st.write("🎧", name)

        with col2:
            if st.button("נגן", key="play_"+path):
                st.session_state.current_file = path

# ======================
# נגן יחיד בלבד (קריטי!)
# ======================
st.divider()

if st.session_state.current_file:
    st.subheader("▶️ נגן")
    st.audio(st.session_state.current_file)
