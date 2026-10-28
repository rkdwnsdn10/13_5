import base64
import struct
import wave
import time
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# 페이지 기본 설정
st.set_page_config(
    page_title="학교 생활 수칙 무한 경고 사이렌",
    page_icon="🚨",
    layout="centered",
)


# pure python으로 사이렌 파동(.wav)을 바이너리로 직접 생성하는 함수
def generate_siren_wav():
    sample_rate = 22050
    duration = 1.0  # 1초 단위 패킷
    num_samples = int(sample_rate * duration)
    
    # WAV 헤더 및 데이터 합성
    raw_data = bytearray()
    for i in range(num_samples):
        t = i / sample_rate
        # 사이렌 파형 계산 (Sweep sound)
        freq = 600 + 400 * (i / num_samples)
        value = int(127 + 120 * ((1 if (int(t * freq * 2) % 2 == 0) else -1)))
        raw_data.append(max(0, min(255, value)))
        
    # 간단한 8-bit Mono WAV 헤더 작성
    wav_header = bytearray()
    wav_header.extend(b'RIFF')
    wav_header.extend(struct.pack('<I', 36 + len(raw_data)))
    wav_header.extend(b'WAVEfmt ')
    wav_header.extend(struct.pack('<I', 16)) # Subchunk1Size
    wav_header.extend(struct.pack('<H', 1))  # AudioFormat (PCM)
    wav_header.extend(struct.pack('<H', 1))  # NumChannels (Mono)
    wav_header.extend(struct.pack('<I', sample_rate)) # SampleRate
    wav_header.extend(struct.pack('<I', sample_rate)) # ByteRate
    wav_header.extend(struct.pack('<H', 1))  # BlockAlign
    wav_header.extend(struct.pack('<H', 8))  # BitsPerSample
    wav_header.extend(b'data')
    wav_header.extend(struct.pack('<I', len(raw_data)))
    
    return base64.b64encode(wav_header + raw_data).decode('utf-8')

# 사이렌 음원 Data URI 사전 생성
SIREN_B64 = generate_siren_wav()


# 세션 상태 관리
if "detection_logs" not in st.session_state:
    st.session_state.detection_logs = []
if "is_alarm_on" not in st.session_state:
    st.session_state.is_alarm_on = False
if "current_rule" not in st.session_state:
    st.session_state.current_rule = ""

# 메인 타이틀
st.title("🚨 학교 생활 수칙 무한 경고 사이렌")
st.caption("경고 버튼을 누르면 정지 버튼을 누를 때까지 크고 강렬한 사이렌 소리가 울립니다.")

# ---------------------------------------------------------
# 경고음 재생 및 끄기 컨트롤러
# ---------------------------------------------------------
if st.session_state.is_alarm_on:
    st.error(f"🚨 **[경고음 작동 중]** 위반 수칙: {st.session_state.current_rule}")
    
    # HTML5 Audio 엘리먼트로 루프 자동 재생 (소리 출력 100% 보장)
    audio_html = f"""
    <div style="text-align: center; margin: 15px 0;">
        <audio autoplay loop controls style="width: 100%;">
            <source src="data:audio/wav;base64,{SIREN_B64}" type="audio/wav">
            브라우저가 오디오 재생을 지원하지 않습니다.
        </audio>
    </div>
    """
    components.html(audio_html, height=70)

    if st.button("🛑 경고음 즉시 끄기 (정지)", type="primary", use_container_width=True):
        st.session_state.is_alarm_on = False
        st.session_state.current_rule = ""
        st.rerun()

    st.markdown("---")

# ---------------------------------------------------------
# 사이드바 제어판
# ---------------------------------------------------------
st.sidebar.header("⚙️ 경고음 제어판")
if st.sidebar.button("🛑 [사이드바] 경고음 끄기", use_container_width=True):
    st.session_state.is_alarm_on = False
    st.session_state.current_rule = ""
    st.rerun()

# ---------------------------------------------------------
# 학교 규칙 위반 경고 버튼 영역
# ---------------------------------------------------------
st.subheader("📢 학교 수칙 위반 원클릭 연속 경고")

col1, col2 = st.columns(2)

with col1:
    # 규칙 1: 욕설 및 비속어
    if st.button("🤬 욕설 / 언어폭력 감지!", use_container_width=True, type="primary"):
        st.session_state.is_alarm_on = True
        st.session_state.current_rule = "🤬 욕설 및 언어폭력"
        log_time = time.strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.detection_logs.insert(0, {
            "시각": log_time,
            "위반 수칙": "🤬 욕설 및 언어폭력",
            "상태": "🚨 비상 사이렌 발령"
        })
        st.rerun()

    st.write("")

    # 규칙 2: 복도 무단 질주 / 고성방가
    if st.button("🏃‍♂️ 복도 질주 / 고성방가!", use_container_width=True):
        st.session_state.is_alarm_on = True
        st.session_state.current_rule = "🏃‍♂️ 복도 질주 / 소란"
        log_time = time.strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.detection_logs.insert(0, {
            "시각": log_time,
            "위반 수칙": "🏃‍♂️ 복도 질주 / 소란",
            "상태": "🚨 사이렌 발령"
        })
        st.rerun()

    st.write("")

    # 규칙 3: 수업 중 스마트폰 무단 사용
    if st.button("📱 수업 중 스마트폰 무단 사용!", use_container_width=True):
        st.session_state.is_alarm_on = True
        st.session_state.current_rule = "📱 수업 중 스마트폰 사용"
        log_time = time.strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.detection_logs.insert(0, {
            "시각": log_time,
            "위반 수칙": "📱 수업 중 스마트폰 사용",
            "상태": "🚨 사이렌 발령"
        })
        st.rerun()

with col2:
    # 규칙 4: 교내 무단 흡연 / 전자담배
    if st.button("🚬 교내 무단 흡연 / 전자담배!", use_container_width=True, type="primary"):
        st.session_state.is_alarm_on = True
        st.session_state.current_rule = "🚬 교내 무단 흡연"
        log_time = time.strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.detection_logs.insert(0, {
            "시각": log_time,
            "위반 수칙": "🚬 교내 무단 흡연",
            "상태": "🚨 비상 사이렌 발령"
        })
        st.rerun()

    st.write("")

    # 규칙 5: 복장 / 교복 규정 위반
    if st.button("👔 교복 / 용의 복장 미흡!", use_container_width=True):
        st.session_state.is_alarm_on = True
        st.session_state.current_rule = "👔 용의 복장 규정 위반"
        log_time = time.strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.detection_logs.insert(0, {
            "시각": log_time,
            "위반 수칙": "👔 용의 복장 규정 위반",
            "상태": "🚨 사이렌 발령"
        })
        st.rerun()

    st.write("")

    # 규칙 6: 기타 학교 규칙 위반
    if st.button("⚠️ 기타 학교 규칙 위반!", use_container_width=True):
        st.session_state.is_alarm_on = True
        st.session_state.current_rule = "⚠️ 기타 수칙 위반
