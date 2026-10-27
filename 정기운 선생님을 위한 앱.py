import streamlit as st
import datetime

# ---------------------------------------------------------
# Page Configuration & CSS Styling
# ---------------------------------------------------------
st.set_page_config(
    page_title="정기운 선생님을 위한 Smart Classroom Dashboard",
    page_icon="🏫",
    layout="wide"
)

# 고급 학교 대시보드 스타일 CSS
st.markdown("""
<style>
    .stApp {
        background-color: #f8fafc;
        background-image: radial-gradient(#e2e8f0 1px, transparent 1px);
        background-size: 20px 20px;
    }
    .school-banner {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
        padding: 25px 20px;
        border-radius: 18px;
        text-align: center;
        box-shadow: 0 8px 15px -3px rgba(30, 58, 138, 0.15);
        margin-bottom: 20px;
    }
    .school-banner h1 {
        font-size: 2.1rem;
        font-weight: 800;
        margin-bottom: 6px;
        color: #ffffff;
    }
    .school-banner p {
        font-size: 1rem;
        color: #e0f2fe;
        margin: 0;
    }
    .top-card {
        background: #ffffff;
        border: 2px solid #cbd5e1;
        padding: 18px 20px;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        text-align: left;
    }
    .top-card-label {
        font-size: 0.9rem;
        color: #475569;
        font-weight: 700;
        margin-bottom: 6px;
    }
    .top-card-val {
        font-size: 1.8rem;
        font-weight: 800;
        color: #1e3a8a;
    }
    .content-box {
        background-color: #ffffff;
        padding: 22px;
        border-radius: 18px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }
    .box-title {
        color: #1e293b;
        font-size: 1.15rem;
        font-weight: 800;
        margin-bottom: 16px;
        border-bottom: 3px solid #3b82f6;
        padding-bottom: 6px;
        display: inline-block;
    }
    .alert-item-warning {
        background-color: #fef3c7;
        color: #92400e;
        padding: 12px 16px;
        border-radius: 10px;
        border-left: 5px solid #f59e0b;
        margin-bottom: 10px;
        font-size: 0.95rem;
    }
    .alert-item-danger {
        background-color: #fee2e2;
        color: #991b1b;
        padding: 12px 16px;
        border-radius: 10px;
        border-left: 5px solid #ef4444;
        margin-bottom: 10px;
        font-size: 0.95rem;
    }
    .alert-item-info {
        background-color: #f3e8ff;
        color: #6b21a8;
        padding: 12px 16px;
        border-radius: 10px;
        border-left: 5px solid #a855f7;
        margin-bottom: 10px;
        font-size: 0.95rem;
    }
    .alert-item-success {
        background-color: #dcfce7;
        color: #166534;
        padding: 12px 16px;
        border-radius: 10px;
        border-left: 5px solid #22c55e;
        margin-bottom: 10px;
        font-size: 0.95rem;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Session State Initialization (기능 페이지 완벽 연동용 세션)
# ---------------------------------------------------------
if "alarm_count" not in st.session_state:
    st.session_state["alarm_count"] = 0

if "demerits" not in st.session_state:
    st.session_state["demerits"] = []

if "anonymous_letters" not in st.session_state:
    st.session_state["anonymous_letters"] = []

if "cleaning_zones" not in st.session_state:
    st.session_state["cleaning_zones"] = {
        "교실 바닥": "확인 필요",
        "책상 주변": "확인 필요",
        "쓰레기통": "확인 필요",
        "분리수거": "확인 필요",
        "칠판·교탁": "확인 필요",
        "창가·사물함": "확인 필요"
    }

# ---------------------------------------------------------
# Sidebar Navigation (첫 번째 이미지의 나열 목록 정확히 반영)
# ---------------------------------------------------------
st.sidebar.markdown("### 🏫 정기운 선생님을 위한 앱")
menu = st.sidebar.radio(
    "페이지 선택:",
    ["📢 메인 페이지", "🔔 경고음", "📋 벌점제도", "📮 익명소통함", "🧹 청소상태 체크 프로그램"]
)

# ---------------------------------------------------------
# PAGE 1: 정기운 선생님을 위한 앱 (메인 페이지)
# ---------------------------------------------------------
if menu == "📢 메인 페이지":
    # 상단 탭 (요청대로 메인 대시보드와 앱 설명 2개만 남김)
    tab1, tab2 = st.tabs(["📊 메인 대시보드", "📖 앱 소개 & 사용 설명"])

    # --- TAB 1: 메인 대시보드 ---
    with tab1:
        st.markdown(f"""
        <div class="school-banner">
            <h1>🏫 1학년 13반 Smart Classroom</h1>
            <p>정기운 선생님을 위한 실시간 학급 관리 통합 대시보드 · {datetime.date.today().strftime("%Y년 %m월 %d일")}</p>
        </div>
        """, unsafe_allow_html=True)

        # 청소 실시간 연동 상태 계산
        total_zones = len(st.session_state["cleaning_zones"])
        clean_zones = [z for z, status in st.session_state["cleaning_zones"].items() if status == "깨끗함"]
        needed_zones = [z for z, status in st.session_state["cleaning_zones"].items() if status == "확인 필요"]
        completion_rate = int((len(clean_zones) / total_zones) * 100)

        # 1. 상단 요약 카운터 Card
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
            <div class="top-card">
                <div class="top-card-label">🔔 오늘 발생 경고음</div>
                <div class="top-card-val">{st.session_state['alarm_count']} 회</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="top-card">
                <div class="top-card-label">💌 도착한 익명 편지</div>
                <div class="top-card-val">{len(st.session_state['anonymous_letters'])} 개</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="top-card">
                <div class="top-card-label">⚠️ 벌점 수여 학생</div>
                <div class="top-card-val">{len(st.session_state['demerits'])} 명</div>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div class="top-card">
                <div class="top-card-label">🧹 청소 필요 구역</div>
                <div class="top-card-val">{len(needed_zones)} 곳</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # 2. 하단 실시간 연동 알림 피드
        left_col, right_col = st.columns([1.2, 0.8])

        with left_col:
            st.markdown('<div class="content-box">', unsafe_allow_html=True)
            st.markdown('<div class="box-title">📢 실시간 학급 주요 알림</div>', unsafe_allow_html=True)
            
            # 1) 청소 상태 연동 알림
            if needed_zones:
                zones_str = ", ".join(needed_zones)
                st.markdown(f"""
                <div class="alert-item-warning">
                    <b>🧹 청소 상태 알림</b><br>
                    {zones_str} 구역 점검이 필요합니다. (청소 완료율: {completion_rate}%)
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="alert-item-success">
                    <b>🧹 청소 완료 알림</b><br>
                    모든 구역 청소가 '깨끗함' 상태입니다! (완료율 100%)
                </div>
                """, unsafe_allow_html=True)

            # 2) 벌점제도 연동 알림
            if st.session_state["demerits"]:
                demerit_details = "<br>".join([f"<b>{d['학생']}</b> 학생 (사유: {d['사유']} / 벌점 {d['벌점']}점)" for d in st.session_state["demerits"]])
                st.markdown(f"""
                <div class="alert-item-danger">
                    <b>⚠️ 벌점 수여 알림</b><br>
                    {demerit_details}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="alert-item-success">
                    <b>⚠️ 벌점 관리 현황</b><br>
                    현재 부과된 벌점 내역이 없습니다.
                </div>
                """, unsafe_allow_html=True)

            # 3) 익명소통함 연동 알림 (0건 시 무알림 처리)
            letter_count = len(st.session_state["anonymous_letters"])
            if letter_count > 0:
                latest = st.session_state["anonymous_letters"][-1]
                st.markdown(f"""
                <div class="alert-item-info">
                    <b>💌 익명소통함 알림</b><br>
                    새로운 편지가 총 <b>{letter_count}건</b> 도착했습니다! (최신: [{latest['category']}] "{latest['content'][:25]}...")
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="alert-item-info">
                    <b>💌 익명소통함 알림</b><br>
                    현재 도착한 익명 편지가 없습니다.
                </div>
                """, unsafe_allow_html=True)

            # 4) 경고음 연동 알림
            st.markdown(f"""
            <div class="alert-item-warning">
                <b>🔔 경고음 발생 알림</b><br>
                오늘 수업 시간 집중 유도 경고음이 총 <b>{st.session_state['alarm_count']}회</b> 발생했습니다.
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

        with right_col:
            st.markdown('<div class="content-box">', unsafe_allow_html=True)
            st.markdown('<div class="box-title">📋 4대 학급 기능 항목 요약</div>', unsafe_allow_html=True)

            st.markdown(f"""
            * **🔔 경고음 카운트**: `{st.session_state['alarm_count']}회` 누적
            * **⚠️ 벌점 관리**: `{len(st.session_state['demerits'])}명` 부과
            * **💌 익명소통함**: `{len(st.session_state['anonymous_letters'])}건` 수신
            * **🧹 청소 평가**: `{len(needed_zones)}구역` 점검 필요 (완료율 `{completion_rate}%`)
            """)

            st.markdown("<hr>", unsafe_allow_html=True)
            st.caption("💡 좌측 사이드바 메뉴에서 각 기능 페이지로 이동하여 직접 데이터를 추가할 수 있습니다.")
            st.markdown('</div>', unsafe_allow_html=True)

    # --- TAB 2: 앱 소개 & 사용 설명 ---
    with tab2:
        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        st.markdown('<div class="box-title">💌 정기운 선생님께 드리는 글</div>', unsafe_allow_html=True)
        
        st.success("""
        ### 👋 매일 학생들을 챙기느라 바쁘신 정기운 선생님!

        저희가 선생님을 위해 선생님을 돕는 앱을 만들었어요.  
        이 앱을 선생님이 잘 이용해 주시기를 바래요.

        이 앱은 총 4가지 기능이 있고 선생님의 필요에 따라 페이지에 들어가서 사용하시면 돼요.  
        잘 사용 하시길 바래요. ✨
        """)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="box-title">📖 앱의 4가지 주요 기능 및 활용법</div>', unsafe_allow_html=True)

        st.markdown("""
        1. **🔔 경고음 기능**: 수업 시간 집중 유도 및 경고음 누적 발생 횟수를 모니터링합니다.
        2. **📋 벌점제도 기능**: 벌점을 받은 학생 수와 구체적인 사유를 한눈에 모니터링합니다.
        3. **📮 익명소통함 기능**: 학생들이 남긴 익명 편지 수량과 고민/건의 내용을 확인합니다.
        4. **🧹 청소상태 체크 프로그램**: 교실 6개 구역의 청소 상태 및 완료율을 실시간으로 확인합니다.
        """)
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# PAGE 2: 경고음 기능 페이지 (메인과 실시간 연동)
# ---------------------------------------------------------
elif menu == "🔔 경고음":
    st.title("🔔 경고음 컨트롤러")
    st.write("수업 시간 집중 유도가 필요할 때 버튼을 클릭하세요. 클릭 횟수가 메인 대시보드에 실시간 연동됩니다.")

    st.subheader(f"오늘 누적 경고음 횟수: {st.session_state['alarm_count']} 회")

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🚨 경고음 울리기 (+1)", use_container_width=True):
            st.session_state["alarm_count"] += 1
            st.toast("🚨 경고음 횟수가 추가되어 메인 대시보드에 반영되었습니다!")
            st.rerun()

    with col_b:
        if st.button("🔄 카운트 리셋 (0회)", use_container_width=True):
            st.session_state["alarm_count"] = 0
            st.toast("경고음 횟수가 초기화되었습니다.")
            st.rerun()

# ---------------------------------------------------------
# PAGE 3: 벌점제도 기능 페이지 (메인과 실시간 연동)
# ---------------------------------------------------------
elif menu == "📋 벌점제도":
    st.title("📋 벌점제도 관리")
    st.write("학생에게 부여한 벌점 내역이 메인 대시보드 알림 피드에 즉시 연동됩니다.")

    with st.form("demerit_form", clear_on_submit=True):
        student = st.text_input("학생 이름")
        reason = st.text_area("벌점 부여 사유")
        points = st.number_input("부여 벌점", min_value=1, max_value=10, value=1)
        
        if st.form_submit_button("벌점 부여 및 대시보드 연동"):
            if student.strip() and reason.strip():
                st.session_state["demerits"].append({
                    "학생": student.strip(),
                    "사유": reason.strip(),
                    "벌점": points
                })
                st.success(f"{student} 학생의 벌점이 등록되어 메인 대시보드에 연동되었습니다!")
                st.rerun()
            else:
                st.warning("학생 이름과 사유를 입력해 주세요.")

    st.markdown("---")
    st.subheader("📜 현재 벌점 부과 목록")
    if st.session_state["demerits"]:
        st.dataframe(st.session_state["demerits"], use_container_width=True)
    else:
        st.info("현재 부과된 벌점 내역이 없습니다.")

# ---------------------------------------------------------
# PAGE 4: 익명소통함 기능 페이지 (메인과 실시간 연동)
# ---------------------------------------------------------
elif menu == "📮 익명소통함":
    st.title("📮 익명소통함 (우리 반 마음우체통)")
    st.write("학생들이 편지를 제출하면 메인 대시보드의 편지 개수가 실시간으로 업데이트됩니다.")

    category = st.selectbox("의견 종류", ["💭 고민 상담", "💡 학급 건의", "👍 칭찬하기", "💬 기타"])
    content = st.text_area("내용을 입력하세요")
    agree = st.checkbox("개인정보를 포함하지 않았음을 확인합니다.")

    if st.button("💌 익명으로 편지 제출하기"):
        if not agree:
            st.warning("동의 체크박스를 눌러주세요.")
        elif not content.strip():
            st.warning("내용을 입력해주세요.")
        else:
            st.session_state["anonymous_letters"].append({
                "category": category,
                "content": content.strip(),
                "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            st.success("편지가 제출되었습니다! 메인 대시보드 알림 카운트에 연동되었습니다.")
            st.rerun()

    st.markdown("---")
    st.subheader("📬 도착한 익명 편지 목록 (선생님 확인용)")
    if st.session_state["anonymous_letters"]:
        for idx, letter in enumerate(reversed(st.session_state["anonymous_letters"])):
            with st.expander(f"✉️ 편지 #{len(st.session_state['anonymous_letters'])-idx} [{letter['category']}] ({letter['date']})"):
                st.write(letter["content"])
    else:
        st.info("현재 도착한 익명 편지가 없습니다.")

# ---------------------------------------------------------
# PAGE 5: 청소상태 체크 프로그램 (메인과 실시간 연동)
# ---------------------------------------------------------
elif menu == "🧹 청소상태 체크 프로그램":
    st.title("🧹 청소상태 체크 프로그램")
    st.write("구역별 청소 상태를 체크하면 메인 대시보드의 완료율과 알림 메시지가 실시간으로 변경됩니다.")

    cols = st.columns(3)
    zones = list(st.session_state["cleaning_zones"].keys())

    for idx, z in enumerate(zones):
        with cols[idx % 3]:
            with st.container(border=True):
                st.markdown(f"### {z}")
                is_clean = st.checkbox("깨끗함 완료", value=(st.session_state["cleaning_zones"][z] == "깨끗함"), key=f"chk_zone_{z}")
                
                new_status = "깨끗함" if is_clean else "확인 필요"
                if new_status != st.session_state["cleaning_zones"][z]:
                    st.session_state["cleaning_zones"][z] = new_status
                    st.rerun()

                status_color = "🟢" if is_clean else "🟡"
                st.write(f"현재 상태: {status_color} **{st.session_state['cleaning_zones'][z]}**")
