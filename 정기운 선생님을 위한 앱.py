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
# Session State Initialization (데이터 상태 및 연동 세팅)
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

# 캡처 화면 기반의 청소 구역별 상태 데이터 세팅
if "cleaning_zones" not in st.session_state:
    st.session_state["cleaning_zones"] = {
        "교실 바닥": {"status": "확인 필요", "last_check": "2026-10-19 02:37"},
        "책상 주변": {"status": "확인 필요", "last_check": "2026-10-19 02:37"},
        "쓰레기통": {"status": "확인 필요", "last_check": "2026-10-19 02:37"},
        "분리수거": {"status": "확인 필요", "last_check": "2026-10-19 02:37"},
        "칠판·교탁": {"status": "확인 필요", "last_check": "2026-10-19 02:37"},
        "창가·사물함": {"status": "확인 필요", "last_check": "2026-10-19 02:37"}
    }

# ---------------------------------------------------------
# Sidebar Navigation
# ---------------------------------------------------------
st.sidebar.title("🏫 정기운 선생님의 학급 앱")
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "이동할 페이지를 선택하세요:",
    ["📢 메인 대시보드", "💌 앱 소개 & 사용 설명", "🔔 경고음 관리", "📋 벌점 관리", "📮 익명 소통함", "🧹 청소 상태 대시보드"]
)

# ---------------------------------------------------------
# Helper Functions (청소 상태 계산 함수)
# ---------------------------------------------------------
def get_cleaning_summary():
    total = len(st.session_state["cleaning_zones"])
    clean_count = sum(1 for z in st.session_state["cleaning_zones"].values() if z["status"] == "깨끗함")
    needed_zones = [name for name, z in st.session_state["cleaning_zones"].items() if z["status"] == "확인 필요"]
    needed_count = len(needed_zones)
    completion_rate = int((clean_count / total) * 100) if total > 0 else 0
    return total, clean_count, needed_count, needed_zones, completion_rate

# ---------------------------------------------------------
# PAGE 1: 메인 대시보드 (스마트폰 알림 센터)
# ---------------------------------------------------------
if page == "📢 메인 대시보드":
    st.title("📱 실시간 학급 대시보드")
    st.caption("2학년 3반 · " + datetime.date.today().strftime("%Y년 %m월 %d일") + " · 학급 통합 대시보드")

    st.info("💡 **정기운 선생님, 환영합니다!** 오늘 학급에서 발생한 주요 현황 요약입니다.")

    total, clean_c, needed_c, needed_zones, comp_rate = get_cleaning_summary()

    st.markdown("### 📊 오늘의 학급 현황 요약")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(label="🔔 오늘 발생 경고음", value=f"{st.session_state['alarm_count']} 회")

    with col2:
        st.metric(label="📮 안 읽은 익명 편지", value=f"{len(st.session_state['anonymous_letters'])} 개")

    with col3:
        st.metric(label="⚠️ 벌점 수여 학생", value=f"{len(st.session_state['demerits'])} 명")

    with col4:
        st.metric(label="🧹 청소 완료율", value=f"{comp_rate}%", delta=f"청소 필요: {needed_c}곳" if needed_c > 0 else "완료")

    st.markdown("---")
    st.subheader("🔔 실시간 학급 알림 피드")

    # 이미지 화면 디자인 반영: 청소 알림 바
    if needed_zones:
        zones_str = ", ".join(needed_zones)
        st.warning(f"🔔 **청소 알림**: {zones_str} 구역의 청소 상태 확인이 필요합니다. (청소 완료율: {comp_rate}%)")
    else:
        st.success("🎉 **청소 알림**: 모든 구역의 청소가 깨끗하게 완료되었습니다! (완료율 100%)")

    # 벌점 학생 상세 알림
    if st.session_state["demerits"]:
        for item in st.session_state["demerits"]:
            st.error(f"⚠️ **[벌점 알림]** {item['학생 이름']} 학생이 '{item['사유']}' 사유로 벌점 **{item['벌점']}점**을 부여받았습니다. ({item['날짜']})")

    # 익명 편지 알림
    if st.session_state["anonymous_letters"]:
        latest_letter = st.session_state["anonymous_letters"][-1]
        st.info(f"📮 **[익명 소통함]** 새로운 편지가 도착했습니다: \"{latest_letter['content'][:25]}...\" ({latest_letter['date']})")

# ---------------------------------------------------------
# PAGE 2: 앱 소개 & 사용 방법
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
       - 교실 바닥, 책상 주변 등 구역별 청소 상태를 실시간 체크하여 완료율과 자동으로 생성되는 **'청소 알림'**을 모니터링할 수 있습니다.
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
# PAGE 6: 청소 상태 대시보드 (첨부 캡처 이미지 구현)
# ---------------------------------------------------------
elif page == "🧹 청소 상태 대시보드":
    st.title("선생님이 말씀하시기 전에, 우리 반이 먼저 움직여요!")
    st.caption("2학년 3반 · " + datetime.date.today().strftime("%Y년 %m월 %d일") + " · 청소 상태 대시보드")

    total, clean_c, needed_c, needed_zones, comp_rate = get_cleaning_summary()

    # 상단 요약 카드 (캡처 이미지 UI 호환)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="깨끗한 구역", value=f"{clean_c}/{total}")
        
    with col2:
        st.metric(label="청소 필요 구역", value=f"{needed_c}곳", delta="↑ 확인 필요" if needed_c > 0 else "완료", delta_color="inverse")
        
    with col3:
        st.metric(label="청소 완료율", value=f"{comp_rate}%")

    st.markdown("<br>", unsafe_allow_html=True)

    # 청소 알림 메시지 박스 생성 (이미지의 알림 바 구현)
    if needed_zones:
        zones_text = ", ".join(needed_zones)
        st.warning(f"🔔 **청소 알림**: {zones_text} 구역을 확인해 주세요.")
    else:
        st.success("🔔 **청소 알림**: 교실의 모든 구역 청소가 완료되었습니다!")

    if st.button("📣 청소 알림 새로고침 / 업데이트", use_container_width=True):
        st.toast("청소 상태 및 알림이 업데이트되었습니다!")
        st.rerun()

    st.markdown("---")
    st.subheader("🧹 구역별 현재 상태 설정")

    # 캡처 이미지 속 구역 타일 레이아웃 생성
    zones_list = list(st.session_state["cleaning_zones"].keys())
    
    # 3개씩 2줄로 배치
    cols1 = st.columns(3)
    for i in range(3):
        z_name = zones_list[i]
        z_data = st.session_state["cleaning_zones"][z_name]
        with cols1[i]:
            with st.container(border=True):
                st.caption("🧹 청소 구역")
                st.markdown(f"### **{z_name}**")
                
                # 상태 변경 토글 버튼/선택
                is_clean = st.checkbox("깨끗함 완료", value=(z_data["status"] == "깨끗함"), key=f"chk_{z_name}")
                
                new_status = "깨끗함" if is_clean else "확인 필요"
                if new_status != z_data["status"]:
                    st.session_state["cleaning_zones"][z_name]["status"] = new_status
                    st.session_state["cleaning_zones"][z_name]["last_check"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                    st.rerun()

                status_icon = "🟢" if is_clean else "🟡"
                st.write(f"{status_icon} **{z_data['status']}**")
                st.caption(f"마지막 확인: {z_data['last_check']}")

    cols2 = st.columns(3)
    for i in range(3, 6):
        z_name = zones_list[i]
        z_data = st.session_state["cleaning_zones"][z_name]
        with cols2[i-3]:
            with st.container(border=True):
                st.caption("🧹 청소 구역")
                st.markdown(f"### **{z_name}**")
                
                is_clean = st.checkbox("깨끗함 완료", value=(z_data["status"] == "깨끗함"), key=f"chk_{z_name}")
                
                new_status = "깨끗함" if is_clean else "확인 필요"
                if new_status != z_data["status"]:
                    st.session_state["cleaning_zones"][z_name]["status"] = new_status
                    st.session_state["cleaning_zones"][z_name]["last_check"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                    st.rerun()

                status_icon = "🟢" if is_clean else "🟡"
                st.write(f"{status_icon} **{z_data['status']}**")
                st.caption(f"마지막 확인: {z_data['last_check']}")
