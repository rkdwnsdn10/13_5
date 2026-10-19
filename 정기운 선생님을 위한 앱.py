import streamlit as st
import datetime

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="정기운 선생님을 위한 Smart Classroom",
    page_icon="🏫",
    layout="wide"
)

# ---------------------------------------------------------
# Session State Initialization (데이터 안전성 보장)
# ---------------------------------------------------------
if "alarm_count" not in st.session_state:
    st.session_state["alarm_count"] = 3

if "demerits" not in st.session_state:
    st.session_state["demerits"] = [
        {"학생 이름": "김철수", "사유": "수업 시간 지각", "벌점": 2, "날짜": "2026-10-19"},
        {"학생 이름": "이영희", "사유": "청소 시간 무단 탈주", "벌점": 3, "날짜": "2026-10-19"}
    ]

if "anonymous_letters" not in st.session_state:
    st.session_state["anonymous_letters"] = [
        {"id": 1, "content": "선생님 항상 수업 재미있게 해주셔서 감사합니다!", "date": "2026-10-18"},
        {"id": 2, "content": "다음 주 학급 체육대회 종목이 궁금해요.", "date": "2026-10-19"},
        {"id": 3, "content": "오늘 자리 배치 바꿔주셔서 정말 좋아요!", "date": "2026-10-19"}
    ]

if "cleaning_status" not in st.session_state:
    st.session_state["cleaning_status"] = "보통"

if "cleaning_logs" not in st.session_state:
    st.session_state["cleaning_logs"] = [
        {"날짜": "2026-10-18", "상태": "좋음", "메모": "칠판 및 창틀 깨끗함"},
        {"날짜": "2026-10-19", "상태": "보통", "메모": "분리수거 확인 필요"}
    ]

# ---------------------------------------------------------
# Sidebar Navigation
# ---------------------------------------------------------
st.sidebar.title("🏫 정기운 선생님의 학급 앱")
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "이동할 페이지를 선택하세요:",
    ["📢 메인 대시보드", "💌 앱 소개 & 사용 설명", "🔔 경고음 관리", "📋 벌점 관리", "📮 익명 소통함", "🧹 청소 상태 체크"]
)

# ---------------------------------------------------------
# PAGE 1: 메인 대시보드
# ---------------------------------------------------------
if page == "📢 메인 대시보드":
    st.title("📱 실시간 학급 대시보드")
    st.caption("핸드폰 알림처럼 학급의 주요 이슈와 현황을 한눈에 확인하세요!")

    st.info("💡 **정기운 선생님, 환영합니다!** 오늘 학급에서 발생한 주요 현황 요약입니다.")

    st.markdown("### 📊 오늘의 학급 현황 요약")
    
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="🔔 오늘 발생 경고음", 
            value=f"{st.session_state['alarm_count']} 회"
        )

    with col2:
        st.metric(
            label="📮 안 읽은 익명 편지", 
            value=f"{len(st.session_state['anonymous_letters'])} 개"
        )

    with col3:
        st.metric(
            label="⚠️ 벌점 수여 학생", 
            value=f"{len(st.session_state['demerits'])} 명"
        )

    with col4:
        status_color = "🟢" if st.session_state['cleaning_status'] == "좋음" else ("🟡" if st.session_state['cleaning_status'] == "보통" else "🔴")
        st.metric(
            label="🧹 오늘의 청소 상태", 
            value=f"{status_color} {st.session_state['cleaning_status']}"
        )

    st.markdown("---")
    st.subheader("🔔 실시간 학급 알림 피드")

    # 벌점 학생 알림
    if st.session_state["demerits"]:
        for item in st.session_state["demerits"]:
            st.warning(f"**[벌점 알림]** {item['학생 이름']} 학생이 '{item['사유']}' 사유로 벌점 **{item['벌점']}점**을 부여받았습니다. ({item['날짜']})")
    else:
        st.success("🎉 오늘 벌점을 받은 학생이 없습니다!")

    # 익명 편지 알림
    if st.session_state["anonymous_letters"]:
        latest_letter = st.session_state["anonymous_letters"][-1]
        st.info(f"**[익명 소통함]** 새로운 편지가 도착했습니다: \"{latest_letter['content'][:25]}...\" ({latest_letter['date']})")

    # 청소 상태 알림
    if st.session_state["cleaning_status"] == "나쁨":
        st.error("**[청소 경고]** 현재 교실 청소 상태가 **'나쁨'**입니다. 점검이 필요합니다!")
    elif st.session_state["cleaning_status"] == "좋음":
        st.success("**[청소 완료]** 오늘 교실 청소 상태가 **'좋음'**으로 아주 쾌적합니다.")

# ---------------------------------------------------------
# PAGE 2: 앱 소개 및 사용 설명
# ---------------------------------------------------------
elif page == "💌 앱 소개 & 사용 설명":
    st.title("💌 정기운 선생님께 드리는 글 & 앱 사용 설명")
    
    st.success("""
    ### 👋 매일 학생들을 챙기느라 바쁘신 정기운 선생님! 

    저희가 선생님을 위해 **선생님을 돕는 앱**을 만들었어요.  
    이 앱을 선생님이 잘 이용해 주시기를 바래요. 

    이 앱은 **총 4가지 기능**이 있고 선생님의 필요에 따라 페이지에 들어가서 사용하시면 돼요.  
    잘 사용 하시길 바래요! ✨
    """)

    st.markdown("---")
    st.subheader("📖 4가지 핵심 기능 및 사용 방법 안내")

    st.markdown("""
    1. **🔔 경고음 기능**
       - 수업 시간 집중 유도나 경고가 필요할 때 버튼을 눌러 경고음 횟수를 누적 및 모니터링합니다.
    2. **📋 벌점 제도 기능**
       - 학생 이름, 사유, 벌점을 작성하면 실시간 대시보드와 관리에 즉각 반영됩니다.
    3. **📮 익명 소통함 기능**
       - 학생들의 고민 편지 수신 및 읽기 조회가 가능합니다.
    4. **🧹 청소 상태 체크 기능**
       - 매일 [좋음 / 보통 / 나쁨] 상태를 기록하여 교실 환경을 관리합니다.
    """)

# ---------------------------------------------------------
# PAGE 3: 경고음 관리
# ---------------------------------------------------------
elif page == "🔔 경고음 관리":
    st.title("🔔 경고음 컨트롤러")
    st.write("수업 집중이나 알림이 필요할 때 사용하세요.")

    st.subheader(f"오늘 누적 경고음 횟수: **{st.session_state['alarm_count']}회**")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚨 경고음 울리기 (+1)", use_container_width=True):
            st.session_state["alarm_count"] += 1
            st.toast("🚨 경고음이 울렸습니다!")
            st.rerun()

    with col2:
        if st.button("🔄 카운트 리셋 (0회)", use_container_width=True):
            st.session_state["alarm_count"] = 0
            st.toast("카운트가 초기화되었습니다.")
            st.rerun()

# ---------------------------------------------------------
# PAGE 4: 벌점 관리
# ---------------------------------------------------------
elif page == "📋 벌점 관리":
    st.title("📋 벌점 관리 시스템")

    st.subheader("➕ 신규 벌점 부여")
    with st.form("demerit_form", clear_on_submit=True):
        student_name = st.text_input("학생 이름")
        reason = st.text_area("벌점 부여 사유")
        points = st.number_input("부여 벌점", min_value=1, max_value=10, value=1)
        
        submitted = st.form_submit_button("벌점 등록")

        if submitted:
            if student_name.strip() and reason.strip():
                today_str = datetime.date.today().strftime("%Y-%m-%d")
                st.session_state["demerits"].append({
                    "학생 이름": student_name.strip(),
                    "사유": reason.strip(),
                    "벌점": points,
                    "날짜": today_str
                })
                st.success(f"{student_name} 학생에게 벌점 {points}점이 등록되었습니다.")
                st.rerun()
            else:
                st.error("학생 이름과 사유를 모두 작성해주세요.")

    st.markdown("---")
    st.subheader("📜 현재 벌점 부과 현황")
    if st.session_state["demerits"]:
        st.dataframe(st.session_state["demerits"], use_container_width=True)
    else:
        st.info("부과된 벌점 내역이 없습니다.")

# ---------------------------------------------------------
# PAGE 5: 익명 소통함
# ---------------------------------------------------------
elif page == "📮 익명 소통함":
    st.title("📮 익명 고민 & 소통함")

    st.subheader("✏️ 익명으로 편지 쓰기")
    letter_text = st.text_area("선생님께 전달할 익명 메시지를 적어주세요.")
    if st.button("편지 보낼게요 💌"):
        if letter_text.strip():
            today_str = datetime.date.today().strftime("%Y-%m-%d")
            new_id = len(st.session_state["anonymous_letters"]) + 1
            st.session_state["anonymous_letters"].append({
                "id": new_id,
                "content": letter_text.strip(),
                "date": today_str
            })
            st.success("익명 편지가 선생님께 전달되었습니다!")
            st.rerun()
        else:
            st.warning("내용을 입력해주세요.")

    st.markdown("---")
    st.subheader("📬 도착한 익명 편지 목록")
    if st.session_state["anonymous_letters"]:
        for letter in reversed(st.session_state["anonymous_letters"]):
            with st.expander(f"✉️ 편지 #{letter['id']} ({letter['date']})"):
                st.write(letter["content"])
    else:
        st.info("도착한 익명 편지가 없습니다.")

# ---------------------------------------------------------
# PAGE 6: 청소 상태 체크
# ---------------------------------------------------------
elif page == "🧹 청소 상태 체크":
    st.title("🧹 오늘의 학급 청소 상태 점검")

    st.subheader("현시점 청소 상태 평가")
    status = st.select_slider(
        "오늘의 교실 청소 상태를 선택해주세요:",
        options=["나쁨", "보통", "좋음"],
        value=st.session_state["cleaning_status"]
    )
    
    note = st.text_input("청소 상태 관련 메모")

    if st.button("청소 상태 저장하기"):
        st.session_state["cleaning_status"] = status
        today_str = datetime.date.today().strftime("%Y-%m-%d")
        st.session_state["cleaning_logs"].append({
            "날짜": today_str,
            "상태": status,
            "메모": note.strip() if note.strip() else "특이사항 없음"
        })
        st.success(f"오늘의 청소 상태가 **'{status}'**(으)로 저장되었습니다.")
        st.rerun()

    st.markdown("---")
    st.subheader("📜 청소 기록 이력")
    st.dataframe(st.session_state["cleaning_logs"], use_container_width=True)
