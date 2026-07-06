import streamlit as st

st.title("בדיקת קובץ ראשי")

st.write("אם אתה רואה את זה → הקובץ נטען")

st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")

st.success("Audio loaded")
"""
import streamlit as st
import os

st.set_page_config(page_title="🎧 סיפורים", layout="wide")

BASE = os.path.dirname(os.path.abspath(__file__))

# ======================
# STATE
# ======================
if "path" not in st.session_state:
    st.session_state.path = BASE

if "search" not in st.session_state:
    st.session_state.search = ""

# ======================
# פונקציות
# ======================
def open_folder(path):
    st.session_state.path = path

def back():
    parent = os.path.dirname(st.session_state.path)
    if os.path.exists(parent):
        st.session_state.path = parent

# ======================
# UI עליון
# ======================
st.title("🎧 ספריית סיפורים")

col1, col2, col3 = st.columns([1, 6, 1])

with col1:
    st.button("⬅️ אחורה", on_click=back)

with col2:
    st.session_state.search = st.text_input("🔍 חיפוש", st.session_state.search)

with col3:
    if st.button("🔄"):
        st.rerun()

st.divider()

current = st.session_state.path

# ======================
# קריאה
# ======================
try:
    items = os.listdir(current)
except Exception as e:
    st.error(e)
    st.stop()

folders = []
mp3s = []

for i in sorted(items):
    full = os.path.join(current, i)

    if os.path.isdir(full):
        folders.append((i, full))
    elif i.lower().endswith(".mp3"):
        mp3s.append((i, full))

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
    st.info("אין תיקיות")
else:
    for name, path in folders:
        c1, c2 = st.columns([6,1])

        with c1:
            st.write("📂", name)

        with c2:
            st.button("פתח", key=path, on_click=open_folder, args=(path,))

st.divider()

# ======================
# MP3 (החלק הקריטי - בלי containers!)
# ======================
st.subheader("🎵 קבצי שמע")

if not mp3s:
    st.info("אין קבצים")
else:
    for name, path in mp3s:
        st.write("🎧", name)
        st.audio(path)
        st.markdown("---")
"""
