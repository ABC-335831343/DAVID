import streamlit as st
import os

st.set_page_config(page_title="🎧 סיפורים", layout="wide")

BASE = os.path.dirname(os.path.abspath(__file__))

# =========================
# STATE
# =========================
if "path" not in st.session_state:
    st.session_state.path = BASE

if "selected" not in st.session_state:
    st.session_state.selected = None

if "search" not in st.session_state:
    st.session_state.search = ""

# =========================
# פונקציות
# =========================
def open_folder(p):
    st.session_state.path = p
    st.session_state.selected = None

def play(p):
    st.session_state.selected = p

def back():
    st.session_state.path = os.path.dirname(st.session_state.path)
    st.session_state.selected = None

# =========================
# UI
# =========================
st.title("🎧 ספריית סיפורים")

c1, c2 = st.columns([1, 6])

with c1:
    st.button("⬅️ אחורה", on_click=back)

with c2:
    st.session_state.search = st.text_input("🔍 חיפוש", st.session_state.search)

st.divider()

path = st.session_state.path

# =========================
# קריאה
# =========================
try:
    items = os.listdir(path)
except:
    st.error("שגיאה בקריאת תיקייה")
    st.stop()

folders = []
mp3s = []

for i in sorted(items):
    full = os.path.join(path, i)

    if os.path.isdir(full):
        folders.append((i, full))
    elif i.lower().endswith(".mp3"):
        mp3s.append((i, full))

# =========================
# חיפוש
# =========================
q = st.session_state.search.lower().strip()

if q:
    folders = [(n,p) for n,p in folders if q in n.lower()]
    mp3s = [(n,p) for n,p in mp3s if q in n.lower()]

# =========================
# תיקיות
# =========================
st.subheader("📁 תיקיות")

for name, full in folders:
    c1, c2 = st.columns([6,1])

    with c1:
        st.write("📂", name)

    with c2:
        st.button("פתח", key=full, on_click=open_folder, args=(full,))

st.divider()

# =========================
# קבצים
# =========================
st.subheader("🎵 MP3")

for name, full in mp3s:
    c1, c2 = st.columns([6,1])

    with c1:
        st.write("🎧", name)

    with c2:
        st.button("▶️", key="p"+full, on_click=play, args=(full,))

# =========================
# נגן יחיד בלבד (קריטי!)
# =========================
st.divider()

if st.session_state.selected:
    st.subheader("▶️ נגן")
    st.audio(st.session_state.selected)
