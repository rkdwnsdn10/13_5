import streamlit as st
import datetime

# ---------------------------------------------------------
# Page Configuration & CSS Styling (학교 일러스트 테마 적용)
# ---------------------------------------------------------
st.set_page_config(
    page_title="정기운 선생님을 위한 Smart Classroom Dashboard",
    page_icon="🏫",
    layout="wide"
)

# 학교 배경 감성 CSS (학교 패턴 및 감성 폰트/카드 디자인)
st.markdown("""
<style>
    /* 학교 교실 분위기의 백그라운드 색상 및 은은한 도트 패턴 */
    .stApp {
        background-color: #f8fafc;
        background-image: radial-gradient(#e2e8f0 1px, transparent 1px);
        background-size: 20px 20px;
    }
    
    /* 대시보드 상단 학교 일러스트 배너 */
    .school-banner {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
        padding: 30px 20px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 10px 15px -3px rgba(30, 58, 138, 0.2);
        margin-bottom: 25px;
        position: relative;
        overflow: hidden;
    }
    .school-banner h1 {
        font-size: 2.3rem;
        font-weight: 800;
        margin-bottom: 8px;
        color: #ffffff;
    }
    .school-banner p {
        font-size: 1.05rem;
        color: #e0f2fe;
        margin: 0;
    }

    /* 상단 네이비 지표 카드 */
    .top-card {
        background: #ffffff;
        border: 2px solid #cbd5e1;
        padding: 18px 20px;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        text-align: left;
        transition: transform 0.2s;
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

    /* 학급 알림 박스 카드 */
    .content-box {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 18px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }
    .box-title {
        color: #1e293b;
        font-size: 1.15rem;
        font-weight: 800;
        margin-bottom: 18px;
        border-bottom: 3px solid #3b82f6;
        padding-bottom: 6px;
        display: inline-block;
    }

    /* 알림 리스트 바 */
    .alert-item-warning {
        background-color: #fef3c7;
        color: #92400e;
        padding: 14px 18px;
        border-radius: 12px;
        border-left: 6px solid #f59e0b;
        margin-bottom: 12px;
        font-size: 0.95rem;
    }
    .alert-item-danger {
        background-color: #fee2e2;
        color: #991b1b;
        padding: 14px 18px;
        border-radius: 12px;
        border-left: 6px solid #ef4444;
        margin-bottom: 12px;
        font-size: 0.95rem;
    }
    .alert-item-info {
        background-color: #f3e8ff;
        color: #6b21a8;
        padding: 14px 18px;
        border-radius: 12px;
        border-left: 6px solid #a855f7;
        margin-bottom: 12px;
        font-size: 0.95rem;
    }
    .alert-item-success {
        background-color: #dcfce7;
        color: #166534;
        padding: 14px 18px;
        border-radius: 12px;
        border-left: 6px solid #22c55e;
        margin-bottom: 12px;
        font-size: 0.95rem;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Session State Initialization (실시간 데이터 연동 전역 관리)
# ---------------------------------------------------------
if "alarm_count" not in st.session_state:
    st.session_state["alarm_count"] = 0  # 초기 0회

if "demerits" not in st.session_state:
    st.session_state["demerits"] = []    # 초기 벌점 목록 없음

if "anonymous_letters" not in st.session_state:
    st.session_state["anonymous_letters"] = []  # 초기 마음우체통 편지 없음 (0건)

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
# 화면 상단 탭 구성
# ---------------------------------------------------------
tabs = st.tabs([
    "📊 대시보드 메인", 
    "💌 우리 반 마음우체통", 
    "🔔 경고음 관리", 
    "📋 벌점 관리", 
    "🧹 청소 대시보드",
    "📖 앱 소개 & 사용 설명"
])

# ---------------------------------------------------------
# TAB 1: 실시간 메인 대시보드 (학교 테마 디자인)
# ---------------------------------------------------------
with tabs[0]:
    # 학교 교실 느낌의 상단 배너
    st.markdown(f"""
    <div class="school-banner">
        <h1>🏫 1학년 13반 Smart Classroom</h1>
        <p>정기운 선생님을 위한 실시간 학급 관리 통합 대시보드 · {datetime.date.today().strftime("%Y년 %m월 %d일")}</p>
    </div>
    """, unsafe_allow_html=True)

    # 청소 상태 연동 계산
    total_zones = len(st.session_state["cleaning_zones"])
    clean_zones = [z for z, status in st.session_state["cleaning_zones"].items() if status == "깨끗함"]
    needed_zones = [z for z, status in st.session_state["cleaning_zones"].items() if status == "확인 필요"]
    completion_rate = int((len(clean_zones) / total_zones) * 100)

    # 1. 상단 요약 카운터
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
            <div class="top-card-label">💌 도착한 마음우체통 편지</div>
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

    # 2. 하단 알림 피드 & 실시간 현황
    left_col, right_col = st.columns([1.2, 0.8])

    with left_col:
        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        st.markdown('<div class="box-title">📢 실시간 학급 주요 알림</div>', unsafe_allow_html=True)
        
        # 1) 청소 상태 실시간 연동 알림
        if needed_zones:
            zones_str = ", ".join(needed_zones)
            st.markdown(f"""
            <div class="alert-item-warning">
                <b>🧹 청소 상태 알림</b><br>
                {zones_str} 구역의 점검이 필요합니다. (청소 완료율: {completion_rate}%)
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="alert-item-success">
                <b>🧹 청소 완료 알림</b><br>
                교실 내 모든 구역 청소가 '깨끗함' 상태입니다! (완료율: 100%)
            </div>
            """, unsafe_allow_html=True)

        # 2) 벌점 실시간 연동 알림
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

        # 3) 마음우체통 실시간 연동 알림 (0건일 때 정확한 문구)
        letter_count = len(st.session_state["anonymous_letters"])
        if letter_count > 0:
            latest = st.session_state["anonymous_letters"][-1]
            st.markdown(f"""
            <div class="alert-item-info">
                <b>💌 우리 반 마음우체통 알림</b><br>
                새로운 편지가 총 <b>{letter_count}건</b> 도착했습니다! (최신: [{latest['category']}] "{latest['content'][:25]}...")
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="alert-item-info">
                <b>💌 우리 반 마음우체통 알림</b><br>
                현재 도착한 익명 편지가 없습니다.
            </div>
            """, unsafe_allow_html=True)

        # 4) 경고음 실시간 연동 알림
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
        * **🔔 경고음 카운트**: `{st.session_state['alarm_count']}회`
        * **⚠️ 벌점 관리**: `{len(st.session_state['demerits'])}명` 부과
        * **💌 우리 반 마음우체통**: `{len(st.session_state['anonymous_letters'])}건` 도착
        * **🧹 청소 평가**: `{len(needed_zones)}구역` 점검 필요 (완료율 `{completion_rate}%`)
        """)

        st.markdown("<hr>", unsafe_allow_html=True)
        st.caption("💡 각 탭에서 데이터를 제출하면 메인 대시보드에 즉시 반영됩니다.")
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 2: 우리 반 마음우체통 (조원 페이지 호환)
# ---------------------------------------------------------
with tabs[1]:
    st.title("📮 우리 반 마음우체통")
    st.caption("이름 없이 전하는 소중한 마음. 고민도, 건의도, 칭찬도 편하게 남겨 주세요.")

    with st.expander("🌼 이용 약속 보기", expanded=True):
        st.write("- 이름이나 학번 등 개인정보는 적지 마세요.")
        st.write("- 욕설, 비하, 협박 등 부적절한 표현은 제한됩니다.")
        st.write("- 서로를 존중하는 표현으로 작성해 주세요.")
        st.write("- 긴급한 문제는 선생님이나 믿을 수 있는 어른에게 직접 알려 주세요.")

    view_mode = st.radio("화면 선택", ["💌 익명 의견 보내기", "🔐 선생님 관리실"])

    if view_mode == "💌 익명 의견 보내기":
        st.subheader("편지 쓰기")
        category = st.selectbox("의견 종류", ["💭 고민 상담", "💡 학급 건의", "👍 친구/선생님 칭찬", "💬 기타 이야기"])
        title = st.text_input("제목 (선택)", placeholder="예: 수업 시간에 건의하고 싶은 점")
        content = st.text_area("전하고 싶은 이야기", placeholder="편하게 이야기해 주세요.")
        agree = st.checkbox("이용 약속을 읽었으며 개인정보를 작성하지 않았습니다.")

        if st.button("💌 익명으로 보내기", use_container_width=True):
            if not agree:
                st.warning("이용 약속 동의 체크박스를 선택해 주세요.")
            elif not content.strip():
                st.warning("전하고 싶은 이야기를 입력해 주세요.")
            else:
                st.session_state["anonymous_letters"].append({
                    "category": category,
                    "title": title.strip() if title.strip() else "제목 없음",
                    "content": content.strip(),
                    "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                })
                st.success("익명 편지가 전송되었습니다! 메인 대시보드에 실시간 반영됩니다.")
                st.rerun()

    else:
        st.subheader("🔐 선생님 전용 편지함")
        if st.session_state["anonymous_letters"]:
            for idx, letter in enumerate(reversed(st.session_state["anonymous_letters"])):
                with st.container(border=True):
                    st.write(f"**[{letter['category']}] {letter['title']}** ({letter['date']})")
                    st.write(letter["content"])
        else:
            st.info("현재 수신된 익명 편지가 없습니다.")

# ---------------------------------------------------------
# TAB 3: 경고음 관리
# ---------------------------------------------------------
with tabs[2]:
    st.title("🔔 경고음 컨트롤러")
    st.subheader(f"오늘 누적 경고음: {st.session_state['alarm_count']} 회")

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🚨 경고음 울리기 (+1)", use_container_width=True):
            st.session_state["alarm_count"] += 1
            st.toast("🚨 경고음이 울렸습니다!")
            st.rerun()
    with col_b:
        if st.button("🔄 카운트 리셋", use_container_width=True):
            st.session_state["alarm_count"] = 0
            st.toast("초기화되었습니다.")
            st.rerun()

# ---------------------------------------------------------
# TAB 4: 벌점 관리
# ---------------------------------------------------------
with tabs[3]:
    st.title("📋 벌점 관리 시스템")
    
    with st.form("demerit_form", clear_on_submit=True):
        student = st.text_input("학생 이름")
        reason = st.text_area("벌점 부여 사유")
        points = st.number_input("부여 벌점", min_value=1, max_value=10, value=1)
        if st.form_submit_button("벌점 부여 및 대시보드 등록"):
            if student.strip() and reason.strip():
                st.session_state["demerits"].append({
                    "학생": student.strip(),
                    "사유": reason.strip(),
                    "벌점": points
                })
                st.success("벌점이 부여되었습니다.")
                st.rerun()
            else:
                st.warning("학생 이름과 사유를 모두 작성해주세요.")

    st.subheader("📜 현재 벌점 부과 목록")
    if st.session_state["demerits"]:
        st.dataframe(st.session_state["demerits"], use_container_width=True)
    else:
        st.info("부과된 벌점이 없습니다.")

# ---------------------------------------------------------
# TAB 5: 청소 상태 대시보드
# ---------------------------------------------------------
with tabs[4]:
    st.title("🧹 청소 상태 대시보드")
    
    cols = st.columns(3)
    zones = list(st.session_state["cleaning_zones"].keys())
    
    for i, z in enumerate(zones):
        with cols[i % 3]:
            with st.container(border=True):
                st.write(f"### {z}")
                is_clean = st.checkbox("깨끗함 완료", value=(st.session_state["cleaning_zones"][z] == "깨끗함"), key=f"clean_{z}")
                new_status = "깨끗함" if is_clean else "확인 필요"
                if new_status != st.session_state["cleaning_zones"][z]:
                    st.session_state["cleaning_zones"][z] = new_status
                    st.rerun()
                st.caption(f"상태: {st.session_state['cleaning_zones'][z]}")

# ---------------------------------------------------------
# TAB 6: 앱 소개 & 사용 설명
# ---------------------------------------------------------
with tabs[5]:
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
    1. **🔔 경고음 기능**: 하루 발생한 누적 경고음 횟수를 모니터링합니다.
    2. **📋 벌점제도 기능**: 벌점을 받은 학생 수와 구체적인 사유를 파악합니다.
    3. **💌 우리 반 마음우체통 기능**: 학생들의 익명 고민/건의/칭찬 편지 수량을 실시간 확인합니다.
    4. **🧹 청소 상태 체크 기능**: 교실 6개 구역의 청소 상태 및 완료율을 체크합니다.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
