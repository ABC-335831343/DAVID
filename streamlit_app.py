import streamlit as st
import os

st.set_page_config(page_title="🎧 סיפורים", layout="wide")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# =====================
# STATE
# =====================
if "path" not in st.session_state:
    st.session_state.path = BASE_DIR

if "search" not in st.session_state:
    st.session_state.search = ""

if "current_audio" not in st.session_state:
    st.session_state.current_audio = None


# =====================
# פונקציות
# =====================
def open_folder(path):
    st.session_state.path = path

def back():
    st.session_state.path = os.path.dirname(st.session_state.path)

def play(file_path):
    st.session_state.current_audio = file_path

def refresh():
    st.rerun()


# =====================
# UI
# =====================
st.title("🎧 נגן סיפורים")

c1, c2, c3 = st.columns([1, 6, 1])

with c1:
    st.button("⬅️ אחורה", on_click=back)

with c2:
    st.session_state.search = st.text_input("🔍 חיפוש", st.session_state.search)

with c3:
    st.button("🔄 רענן", on_click=refresh)

st.divider()

path = st.session_state.path

# =====================
# קריאה
# =====================
items = os.listdir(path)

folders = []
mp3s = []

for i in sorted(items):
    full = os.path.join(path, i)

    if os.path.isdir(full):
        folders.append((i, full))
    elif i.lower().endswith(".mp3"):
        mp3s.append((i, full))


# =====================
# חיפוש
# =====================
q = st.session_state.search.lower().strip()

if q:
    folders = [(n,p) for n,p in folders if q in n.lower()]
    mp3s = [(n,p) for n,p in mp3s if q in n.lower()]


# =====================
# תיקיות
# =====================
st.subheader("📁 תיקיות")

if not folders:
    st.info("אין תיקיות")
else:
    for name, full in folders:
        c1, c2 = st.columns([6,1])

        with c1:
            st.write("📂", name)

        with c2:
            st.button("פתח", key=full, on_click=open_folder, args=(full,))


st.divider()

# =====================
# MP3 LIST
# =====================
st.subheader("🎵 קבצים")

if not mp3s:
    st.info("אין קבצים")
else:
    for name, full in mp3s:
        c1, c2 = st.columns([6,1])

        with c1:
            st.write("🎧", name)

        with c2:
            st.button("▶️ נגן", key="p_"+full, on_click=play, args=(full,))


# =====================
# PLAYER (רק אחד!)
# =====================
if st.session_state.current_audio:
    st.divider()
    st.subheader("▶️ נגן פעיל")
    st.audio(st.session_state.current_audio)
