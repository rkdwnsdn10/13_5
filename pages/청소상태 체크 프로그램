import streamlit as st
import random
import time

# 1. 페이지 설정 및 디자인 (테마 컬러: 청결하고 깔끔한 민트/블루)
st.set_page_config(
    page_title="우리 반 청소 상태 체크기",
    page_icon="🧹",
    layout="wide",
)

# 커스텀 스타일 적용 (CSS)
st.markdown("""
<style>
    .main-title { font-size: 2.5rem; font-weight: bold; color: #2E7D32; text-align: center; margin-bottom: 20px; }
    .subtitle { font-size: 1.1rem; color: #555555; text-align: center; margin-bottom: 30px; }
    .area-box { padding: 15px; border-radius: 10px; background-color: #F1F8E9; border-left: 5px solid #8BC34A; margin-bottom: 15px; }
    .alert-box { padding: 20px; border-radius: 10px; background-color: #FFEBEE; border: 2px solid #EF5350; text-align: center; color: #C62828; font-size: 1.3rem; font-weight: bold; animation: blinker 1.5s linear infinite; }
    @keyframes blinker { 50% { opacity: 0.5; } }
</style>
""", unsafe_allow_html=True)

# 2. 세션 상태(Session State) 초기화 - 데이터 유지용
if "cleaning_data" not in st.session_state:
    st.session_state.cleaning_data = {
        "칠판 및 교탁": {"checked": False, "score": 3, "checker": ""},
        "책상 및 의자 정돈": {"checked": False, "score": 3, "checker": ""},
        "바닥 비질 및 걸레질": {"checked": False, "score": 3, "checker": ""},
        "쓰레기통 및 분리수거": {"checked": False, "score": 3, "checker": ""},
        "창틀 및 사물함 위": {"checked": False, "score": 3, "checker": ""}
    }

if "alert_triggered" not in st.session_state:
    st.session_state.alert_triggered = False

if "history" not in st.session_state:
    st.session_state.history = []

# 3. 앱 타이틀 및 소개
st.markdown("<div class='main-title'>✨ 우리 반 청소 상태 체크 프로그램 ✨</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>간편하게 청소 상태를 점검하고, 미흡한 곳은 화면 알림을 통해 빠르게 인지하세요!</div>", unsafe_allow_html=True)

# 4. 화면 레이아웃 분할
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("📋 실시간 청소 구역별 점검")
    
    # 예외 처리: 데이터 구조 검증
    try:
        for area, info in st.session_state.cleaning_data.items():
            with st.container():
                st.markdown(f"<div class='area-box'><b>🔍 점검 구역: {area}</b></div>", unsafe_allow_html=True)
                
                # 가로로 정렬하여 입력 받기
                c1, c2, c3 = st.columns([2, 2, 3])
                with c1:
                    info["checked"] = st.checkbox("점검 완료", value=info["checked"], key=f"check_{area}")
                with c2:
                    info["score"] = st.slider("청결 점수 (1~5점)", min_value=1, max_value=5, value=info["score"], key=f"score_{area}")
                with c3:
                    info["checker"] = st.text_input("확인 학생 이름", value=info["checker"], key=f"name_{area}", placeholder="이름 입력")
                st.write("---")
    except Exception as e:
        st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")

with col2:
    st.subheader("🚨 청소 상태 알림판")
    
    # 미흡한 구역 찾기 (점수가 2점 이하이거나, 점검 완료가 안 된 구역 확인)
    incomplete_areas = [area for area, info in st.session_state.cleaning_data.items() if not info["checked"]]
    poor_areas = [area for area, info in st.session_state.cleaning_data.items() if info["checked"] and info["score"] <= 2]
    
    # 알림 로직 트리거
    if incomplete_areas or poor_areas:
        st.session_state.alert_triggered = True
        st.markdown("<div class='alert-box'>⚠️ 주의: 아직 청소가 미흡하거나 점검되지 않은 구역이 있습니다!</div>", unsafe_allow_html=True)
        
        if incomplete_areas:
            st.warning(f"📌 **아직 점검 전 구역:** {', '.join(incomplete_areas)}")
        if poor_areas:
            st.error(f"🧹 **재청소 필요 구역 (2점 이하):** {', '.join(poor_areas)}")
    else:
        st.session_state.alert_triggered = False
        st.success("🎉 모든 구역의 청소가 완벽하게 완료되었습니다! 참 잘했어요!")
        st.balloons()

    # 5. 최종 확인 및 히스토리 저장
    st.subheader("💾 오늘 하루 기록하기")
    submit_btn = st.button("🌟 오늘 청소 최종 제출하기", use_container_width=True)
    
    if submit_btn:
        total_score = sum([info["score"] for info in st.session_state.cleaning_data.values() if info["checked"]])
        checked_count = sum([1 for info in st.session_state.cleaning_data.values() if info["checked"]])
        
        if checked_count == 0:
            st.error("최소 한 곳 이상의 구역을 점검 완료해야 제출할 수 있습니다.")
        else:
            avg_score = round(total_score / checked_count, 2)
            today_record = {
                "time": time.strftime("%Y-%m-%d %H:%M:%S"),
                "score": avg_score,
                "status": "완벽" if not (incomplete_areas or poor_areas) else "보완 필요"
            }
            st.session_state.history.append(today_record)
            st.success(f"제출 완료! 오늘 평균 청소 점수는 **{avg_score}점**입니다.")

    # 저장된 기록 보기
    if st.session_state.history:
        st.write("📆 **최근 청소 기록 내역**")
        for h in reversed(st.session_state.history):
            st.info(f"🕒 {h['time']} | 평균 점수: {h['score']}점 | 상태: {h['status']}")

# 6. 리셋 버튼 (초기화)
if st.button("🔄 전체 입력 초기화"):
    st.session_state.cleaning_data = {
        "칠판 및 교탁": {"checked": False, "score": 3, "checker": ""},
        "책상 및 의자 정돈": {"checked": False, "score": 3, "checker": ""},
        "바닥 비질 및 걸레질": {"checked": False, "score": 3, "checker": ""},
        "쓰레기통 및 분리수거": {"checked": False, "score": 3, "checker": ""},
        "창틀 및 사물함 위": {"checked": False, "score": 3, "checker": ""}
    }
    st.rerun()
