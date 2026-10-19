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
    c.metric("청소 완료율", f"{completion}%")

    if pending:
        st.warning("🔔 청소 알림: " + ", ".join(pending) + " 구역을 확인해 주세요.")
        if st.button("📣 청소 알림 만들기", use_container_width=True):
            add_notification("청소가 필요한 구역: " + ", ".join(pending) + " — 담당 친구들과 함께 정리해 주세요!")
            st.success("알림 기록에 추가했어요.")
    else:
        st.success("✨ 모든 구역이 깨끗해요! 지금 상태를 유지해 주세요.")

    st.markdown("## 구역별 현재 상태")
    cols = st.columns(3)
    for i, area in enumerate(AREAS):
        info = st.session_state.areas[area]
        with cols[i % 3]:
            st.markdown(f"""<div class="cc-card">
            <div class="cc-small">{'🧹 청소 구역'}</div>
            <h3 style="margin:.35rem 0">{area}</h3>
            <div style="font-size:1.05rem">{show_status(info['status'])}</div>
            <div class="cc-small">마지막 확인: {info['updated']}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("## 다음 알림 시간")
    lunch = st.session_state.settings["lunch_time"].strftime("%H:%M")
    dismiss = st.session_state.settings["dismissal_time"].strftime("%H:%M")
    x, y = st.columns(2)
    x.info(f"🍱 점심시간 점검 · {lunch}")
    y.info(f"🏫 종례 전 점검 · {dismiss}")
    st.caption("이 배포 버전은 예약 시간에 자동으로 푸시 알림이나 방송을 보내지 않아요. 정해진 시간에 앱을 열어 상태를 확인하고 알림을 기록하는 시연용 기능입니다.")

# ---------- 청소 점검 ----------
elif page == "🧽 청소 점검":
    st.title("🧽 청소 상태 점검")
    st.write("센서가 연결되어 있다면 센서값으로 상태를 갱신하고, 현재는 시연을 위해 직접 상태를 선택할 수 있어요.")
    with st.expander("센서 연결 안내"):
        st.write("실제 센서 자동 감지에는 센서(예: 먼지·무게·거리 센서), 데이터를 앱으로 보내는 장치(예: ESP32), 그리고 안전한 데이터 수신 주소가 필요합니다. 아래 수동 상태는 실제 센서 측정값이 아닙니다.")
    selected_area = st.selectbox("점검할 구역", AREAS)
    current = st.session_state.areas[selected_area]
    with st.form("area_check_form"):
        new_status = st.radio("현재 상태", STATUSES, index=STATUSES.index(current["status"]), horizontal=True)
        note = st.text_input("점검 메모 (선택)", value=current.get("note", ""), placeholder="예: 바닥에 종이 조각이 있어요")
        submitted = st.form_submit_button("상태 저장", use_container_width=True)
    if submitted:
        st.session_state.areas[selected_area] = {"status": new_status, "note": note.strip(), "updated": now_string()}
        record_event(selected_area, new_status, note.strip())
        if new_status != "깨끗함":
            add_notification(f"{selected_area}: {new_status}. 청소 상태를 확인해 주세요.")
        st.success(f"{selected_area} 상태를 저장했어요.")
        st.rerun()

    st.markdown("### 전체 구역 빠른 점검")
    for area in AREAS:
        info = st.session_state.areas[area]
        with st.container(border=True):
            left, mid, right = st.columns([2, 2, 1])
            left.markdown(f"**{area}**")
            mid.write(show_status(info["status"]))
            if right.button("깨끗함으로", key=f"clean_{area}"):
                st.session_state.areas[area] = {"status": "깨끗함", "note": "", "updated": now_string()}
                record_event(area, "깨끗함", "빠른 점검으로 완료 처리")
                st.success(f"{area} 청소 완료!")
                st.rerun()

# ---------- 알림 ----------
elif page == "🔔 알림 관리":
    st.title("🔔 청소 알림 관리")
    st.write("청소가 필요한 구역을 학생들이 스스로 확인할 수 있도록 안내 문구를 만들고 기록해요.")
    pending = pending_areas()
    st.markdown("### 알림 문구 미리보기")
    if pending:
        message = "우리 반 청소 시간이에요! " + ", ".join(pending) + " 구역을 함께 정리해 주세요. 청소 후 앱에서 상태를 확인해 주세요. 💙"
    else:
        message = "우리 반 청소 상태가 모두 양호해요! 깨끗한 교실을 함께 유지해요. 💙"
    st.info(message)
    if st.button("알림 기록에 추가", use_container_width=True):
        add_notification(message)
        st.success("알림을 기록했어요.")
    st.caption("기기에서 소리를 자동 재생하거나 실제 교실 방송을 울리는 기능은 포함되어 있지 않습니다. 브라우저 자동재생 제한 및 별도 스피커/방송 장치 연동이 필요합니다.")

    st.markdown("### 알림 기록")
    if st.session_state.notifications:
        for item in st.session_state.notifications[:20]:
            with st.container(border=True):
                st.caption(item["시간"])
                st.write("🔔 " + item["알림"])
    else:
        st.info("아직 알림 기록이 없어요.")

# ---------- 기록 ----------
elif page == "📋 기록":
    st.title("📋 청소 점검 기록")
    if st.session_state.records:
        df = pd.DataFrame(st.session_state.records)
        area_filter = st.selectbox("구역 필터", ["전체"] + AREAS)
        if area_filter != "전체":
            df = df[df["구역"] == area_filter]
        st.dataframe(df, use_container_width=True, hide_index=True)
        csv = df.to_csv(index=False).encode("utf-8-sig")
        st.download_button("⬇️ 기록 CSV 다운로드", data=csv, file_name="cleanclass_records.csv", mime="text/csv", use_container_width=True)
        if st.button("점검 기록 모두 지우기"):
            st.session_state.records = []
            st.rerun()
    else:
        st.info("아직 점검 기록이 없어요. '청소 점검' 메뉴에서 상태를 저장해 주세요.")

# ---------- 통계 ----------
elif page == "📊 통계":
    st.title("📊 청소 통계")
    clean_count = sum(1 for x in st.session_state.areas.values() if x["status"] == "깨끗함")
    summary = pd.DataFrame({
        "구역": AREAS,
        "깨끗함": [1 if st.session_state.areas[a]["status"] == "깨끗함" else 0 for a in AREAS],
        "확인 필요": [1 if st.session_state.areas[a]["status"] == "확인 필요" else 0 for a in AREAS],
        "청소 필요": [1 if st.session_state.areas[a]["status"] == "청소 필요" else 0 for a in AREAS],
    }).set_index("구역")
    st.metric("현재 청소 완료율", f"{round(clean_count / len(AREAS) * 100)}%")
    st.markdown("### 구역별 상태")
    st.bar_chart(summary)
    if st.session_state.records:
        record_df = pd.DataFrame(st.session_state.records)
        record_df["날짜"] = record_df["시간"].str.slice(0, 10)
        daily = record_df.groupby(["날짜", "상태"]).size().unstack(fill_value=0)
        st.markdown("### 날짜별 점검 기록 수")
        st.line_chart(daily)
    else:
        st.caption("점검 기록이 쌓이면 날짜별 변화도 확인할 수 있어요.")

# ---------- 규칙 ----------
elif page == "📘 규칙 안내":
    st.title("📘 우리 반 청소 약속")
    st.markdown("""<div class="cc-card"><h3>💙 청소는 벌점이 아니라 함께 만드는 약속!</h3>
    청소 알림은 누구를 혼내기 위한 것이 아니라, 필요한 일을 미리 알려 모두가 함께 움직이도록 돕기 위한 기능이에요.</div>""", unsafe_allow_html=True)
    rules = [
        ("1", "알림을 보면 먼저 주변을 확인해요."),
        ("2", "내가 맡은 구역을 안전하게 정리해요."),
        ("3", "쓰레기는 종류에 맞게 분리배출해요."),
        ("4", "청소 도구는 사용 후 제자리에 놓아요."),
        ("5", "끝나면 구역 상태를 다시 확인해요."),
        ("6", "혼자 하기 어려운 일은 친구나 선생님께 도움을 요청해요."),
    ]
    for number, rule in rules:
        st.markdown(f"""<div class="cc-card" style="padding:12px 16px;margin-bottom:8px">
        <b style="color:#526fe0;font-size:1.1rem">{number}</b>　{rule}</div>""", unsafe_allow_html=True)

# ---------- 설정 ----------
elif page == "⚙️ 설정":
    st.title("⚙️ 교실 설정")
    settings = st.session_state.settings
    with st.form("settings_form"):
        class_name = st.text_input("학급 이름", value=settings["class_name"], max_chars=30)
        lunch_time = st.time_input("점심시간 점검 시간", value=settings["lunch_time"])
        dismissal_time = st.time_input("종례 전 점검 시간", value=settings["dismissal_time"])
        reminder_enabled = st.checkbox("알림 기능 사용", value=settings["reminder_enabled"])
        saved = st.form_submit_button("설정 저장", use_container_width=True)
    if saved:
        if not class_name.strip():
            st.error("학급 이름을 입력해 주세요.")
        else:
            st.session_state.settings = {
                "class_name": class_name.strip(),
                "lunch_time": lunch_time,
                "dismissal_time": dismissal_time,
                "reminder_enabled": reminder_enabled,
            }
            st.success("설정을 저장했어요.")
            st.rerun()
    st.markdown("### 데이터 안내")
    st.warning("이 기본 버전의 데이터는 현재 브라우저 세션에 저장됩니다. 앱을 새로 시작하거나 세션이 초기화되면 기록이 사라질 수 있어요. 여러 기기에서 공유하거나 영구 보관하려면 데이터베이스 연결이 필요합니다.")

st.markdown("---")
st.caption("클린클래스 · 파란 교실 청소 알림 시연 앱 | 실제 센서·방송 연결 전에는 수동 점검 모드로 작동합니다.")
