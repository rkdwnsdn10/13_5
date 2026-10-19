import streamlit as st
import random
import time
from datetime import datetime
import google.generativeai as genai
from PIL import Image

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="우리반 스마트 청소 반장",
    page_icon="🧹",
    layout="wide"
)

# 2. Gemini AI 설정 및 예외 처리
ai_available = False
if "GEMINI_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # 가벼운 텍스트/이미지 처리를 위해 gemini-2.5-flash-lite 사용
        model = genai.GenerativeModel('gemini-2.5-flash-lite')
        ai_available = True
    except Exception as e:
        st.warning(f"AI 모델 로드 실패 (기본 기능으로 동작합니다): {e}")
else:
    st.info("💡 팁: Streamlit Secrets에 GEMINI_API_KEY를 등록하면 AI 청소 검사 기능을 사용할 수 있습니다.")

# 3. 세션 상태(State) 초기화
if "sensor_dust" not in st.session_state:
    st.session_state.sensor_dust = random.randint(15, 80)
if "sensor_floor" not in st.session_state:
    st.session_state.sensor_floor = random.randint(20, 90)
if "sensor_trash" not in st.session_state:
    st.session_state.sensor_trash = random.randint(10, 85)

# 타이틀 및 인트로
st.title("🧹 우리반 스마트 청소 상태 체크 시스템")
st.markdown("##### 선생님이 오시기 전에! 센서 데이터를 확인하고 깨끗한 교실을 만들어요.")

# 좌우 레이아웃 분할
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("📊 실시간 교실 센서 모니터링")
    
    # 실제 IoT 센서 대신 데모용 값을 조절하거나 새로고침할 수 있는 기능
    if st.button("🔄 센서 데이터 동기화 (새로고침)"):
        st.session_state.sensor_dust = random.randint(15, 80)
        st.session_state.sensor_floor = random.randint(20, 90)
        st.session_state.sensor_trash = random.randint(10, 85)
        st.rerun()
        
    # 센서 값 표시
    dust = st.session_state.sensor_dust
    floor = st.session_state.sensor_floor
    trash = st.session_state.sensor_trash
    
    # 종합 점수 계산 (낮을수록 더럽고, 높을수록 깨끗함)
    # 각 센서 수치는 오염도를 뜻하므로 100에서 차감
    clean_score = int(100 - (dust*0.3 + floor*0.4 + trash*0.3))
    
    # 메트릭 표시
    m1, m2, m3 = st.columns(3)
    m1.metric("🌬️ 미세먼지 수치", f"{dust} µg/m³", "나쁨" if dust > 50 else "좋음", delta_color="inverse")
    m2.metric("👟 바닥 먼지/자국", f"{floor} %", "더러움" if floor > 60 else "깨끗함", delta_color="inverse")
    m3.metric("🗑️ 쓰레기통 적재량", f"{trash} %", "비워야함" if trash > 70 else "여유", delta_color="inverse")

    st.markdown("---")
    st.subheader("📢 청소 알림 및 스케줄러")
    
    # 시간 조건 설정
    current_time = datetime.now().strftime("%H:%M")
    st.write(f"⏰ 현재 교실 시계: **{current_time}**")
    
    alert_time_option = st.selectbox(
        "🔔 알림을 울릴 타이밍을 선택하세요:",
        ["점심시간 전 (12:30)", "종례 전 (15:20)", "지금 당장 테스트 알림 울리기"]
    )
    
    # 청소 상태 판별 및 알림 발송 조건
    is_time_to_clean = False
    if alert_time_option == "지금 당장 테스트 알림 울리기":
        is_time_to_clean = True
    elif alert_time_option == "점심시간 전 (12:30)" and "12:20" <= current_time <= "12:40":
        is_time_to_clean = True
    elif alert_time_option == "종례 전 (15:20)" and "15:10" <= current_time <= "15:30":
        is_time_to_clean = True

    if is_time_to_clean:
        if clean_score < 70:
            st.error(f"🚨🚨 [청소 경보] 현재 청소 점수 **{clean_score}점**! 교실이 지저분합니다. 선생님이 오시기 전에 청소 시작하세요! 🚨🚨")
            # 브라우저 오디오 알림 (경고음) 효과 적용
            st.audio("https://google.com", format="audio/ogg")
        else:
            st.success(f"✨ 우리 반 현재 청소 점수 **{clean_score}점**으로 매우 양호합니다! 이대로 유지하세요! 🎉")
            st.balloons()
    else:
        st.info("💡 아직 지정된 알림 시간이 아닙니다. 설정된 시간이 되면 자동으로 점수를 체크해 경보를 울립니다.")

with col2:
    st.subheader("🤖 AI 청소 확인원 (선택)")
    st.write("청소를 완료한 구역(칠판, 바닥, 책상 등) 사진을 찍어 올리면 AI가 상태를 정밀 진단해 줍니다.")
    
    uploaded_file = st.file_uploader("📸 청소 인증샷 올리기", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='업로드된 학급 사진', use_container_width=True)
        
        if st.button("🧐 AI에게 검사받기"):
            if not ai_available:
                st.error("Secrets에 'GEMINI_API_KEY'가 설정되지 않아 검사 기능을 이용할 수 없습니다.")
            else:
                with st.spinner("AI가 교실 바닥과 상태를 꼼꼼히 확인하고 있습니다..."):
                    try:
                        prompt = (
                            "너는 중고등학교 학급의 엄격하면서도 친절한 청소 지도 선생님이야. "
                            "제공된 사진을 보고 청소 상태를 분석해줘. "
                            "잘된 점과 미흡해서 더 쓸고 닦아야 할 점을 10대 학생들이 이해하기 쉽게 친근한 어조로 나눠서 피드백해줘. "
                            "마지막에는 100점 만점 중에 청소 점수를 몇 점 줄 수 있는지 명시해줘."
                        )
                        response = model.generate_content([prompt, image])
                        st.markdown("### 📋 AI 검사 결과 보고서")
                        st.write(response.text)
                    except Exception as e:
                        st.error(f"AI 분석 중 오류가 발생했습니다: {e}")

# 하단 가이드라인
st.markdown("---")
st.caption("🏫 Smart School Cleaning Assistant v1.0 | 가상 IoT 센서 연동 프로토타입")
