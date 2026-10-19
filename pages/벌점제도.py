import streamlit as st
import pandas as pd
from datetime import datetime, date, time

st.set_page_config(
    page_title="클린클래스 | 우리 반 청소 알림",
    page_icon="🧹",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- 스타일 ----------
st.markdown("""
<style>
:root { --blue:#526fe0; --blue2:#7894f4; --pale:#edf3ff; --ink:#172b55; }
.stApp { background: linear-gradient(145deg, #eaf3ff 0%, #f7faff 48%, #e7f0ff 100%); color:var(--ink); }
[data-testid="stHeader"] { background: rgba(234,243,255,.85); }
[data-testid="stSidebar"] { background: linear-gradient(180deg,#dce9ff,#f2f7ff); border-right:1px solid #cbdafa; }
.block-container { padding-top: 1.5rem; padding-bottom: 2rem; max-width: 1250px; }
h1,h2,h3 { color:#17366d !important; }
div[data-testid="stMetric"] { background:rgba(255,255,255,.86); border:1px solid #d6e2fb; padding:16px; border-radius:18px; box-shadow:0 4px 14px rgba(62,95,160,.08); }
div.stButton > button { border-radius:12px; border:1px solid #b8c9fb; background:#526fe0; color:white; font-weight:700; }
div.stButton > button:hover { background:#3f5dcc; border-color:#3f5dcc; color:white; }
div[data-testid="stForm"] { background:rgba(255,255,255,.75); padding:16px; border-radius:16px; border:1px solid #d6e2fb; }
.cc-card { background:rgba(255,255,255,.9); border:1px solid #d8e4fb; border-radius:18px; padding:18px; margin-bottom:12px; box-shadow:0 4px 15px rgba(51,85,150,.06); }
.cc-small { color:#5c7198; font-size:.9rem; }
.cc-pill { display:inline-block; background:#e7edff; color:#3655c6; padding:5px 10px; border-radius:999px; font-weight:700; font-size:.85rem; }
</style>
""", unsafe_allow_html=True)

AREAS = ["교실 바닥", "책상 주변", "쓰레기통", "분리수거", "칠판·교탁", "창가·사물함"]
STATUSES = ["깨끗함", "확인 필요", "청소 필요"]
STATUS_EMOJI = {"깨끗함": "🟢", "확인 필요": "🟡", "청소 필요": "🔴"}

def now_string():
    return datetime.now().strftime("%Y-%m-%d %H:%M")

if "areas" not in st.session_state:
    st.session_state.areas = {area: {"status": "확인 필요", "note": "", "updated": now_string()} for area in AREAS}
if "records" not in st.session_state:
    st.session_state.records = []
if "notifications" not in st.session_state:
    st.session_state.notifications = []
if "settings" not in st.session_state:
    st.session_state.settings = {
        "class_name": "2학년 3반",
        "lunch_time": time(12, 20),
        "dismissal_time": time(14, 40),
        "reminder_enabled": True,
    }

def record_event(area, status, note=""):
    st.session_state.records.insert(0, {
        "시간": now_string(), "구역": area, "상태": status, "메모": note
    })
    st.session_state.records = st.session_state.records[:300]

def pending_areas():
    return [a for a, info in st.session_state.areas.items() if info["status"] != "깨끗함"]

def add_notification(message):
    st.session_state.notifications.insert(0, {"시간": now_string(), "알림": message})
    st.session_state.notifications = st.session_state.notifications[:100]

def show_status(status):
    return f"{STATUS_EMOJI.get(status, '⚪')} {status}"

# ---------- 사이드바 ----------
with st.sidebar:
    st.markdown("# 🧹 클린클래스")
    st.caption("우리 반 청소 알림 시스템")
    st.markdown("---")
    page = st.radio(
        "메뉴",
        ["🏠 홈", "🧽 청소 점검", "🔔 알림 관리", "📋 기록", "📊 통계", "📘 규칙 안내", "⚙️ 설정"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown("**오늘의 청소 상태**")
    clean_count = sum(1 for x in st.session_state.areas.values() if x["status"] == "깨끗함")
    st.progress(clean_count / len(AREAS))
    st.caption(f"{clean_count}/{len(AREAS)}개 구역 깨끗함")
    st.caption("※ 현재는 시연용 수동 점검 모드")

# ---------- 홈 ----------
if page == "🏠 홈":
    st.markdown("# 🧹 클린클래스")
    st.markdown("### 선생님이 말씀하시기 전에, 우리 반이 먼저 움직여요!")
    st.caption(f"{st.session_state.settings['class_name']} · {date.today().strftime('%Y년 %m월 %d일')} · 청소 상태 대시보드")

    pending = pending_areas()
    clean_count = len(AREAS) - len(pending)
    completion = round(clean_count / len(AREAS) * 100)
    a, b, c = st.columns(3)
    a.metric("깨끗한 구역", f"{clean_count}/{len(AREAS)}")
    b.metric("청소 필요 구역", f"{len(pending)}곳", delta="확인 필요" if pending else "모두 깨끗해요", delta_color="inverse" if pending else "normal")
