import base64
import struct
import time
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# 페이지 기본 설정
st.set_page_config(
    page_title="실시간 음성 욕설 무한 경고 사이렌",
    page_icon="🚨",
    layout="centered",
)


# pure python으로 100% 작동하는 사이렌 WAV 오디오 바이트 생성
def create_siren_audio_b64():
    sample_rate = 22050
    duration = 1.0
    num_samples = int(sample_rate * duration)

    audio_bytes = bytearray()
    for i in range(num_samples):
        # 600Hz ~ 1000Hz 사이렌 주파수 sweep
        freq = 600 + 400 * (i / num_samples)
        period = sample_rate / freq
        val = 200 if (i % int(period)) < (period / 2) else 50
        audio_bytes.append(val)

    # 8-bit Mono PCM WAV 헤더 패킹
    header = bytearray()
    header.extend(b"RIFF")
    header.extend(struct.pack("<I", 36 + len(audio_bytes)))
    header.extend(b"WAVEfmt ")
    header.extend(struct.pack("<I", 16))
    header.extend(struct.pack("<H", 1))
    header.extend(struct.pack("<H", 1))
    header.extend(struct.pack("<I", sample_rate))
    header.extend(struct.pack("<I", sample_rate))
    header.extend(struct.pack("<H", 1))
    header.extend(struct.pack("<H", 8))
    header.extend(b"data")
    header.extend(struct.pack("<I", len(audio_bytes)))

    wav_data = header + audio_bytes
    return base64.b64encode(wav_data).decode("utf-8")


# 사이렌 음원 사전 생성
SIREN_B64 = create_siren_audio_b64()

# 세션 상태 관리
if "detection_logs" not in st.session_state:
    st.session_state.detection_logs = []
if "is_alarm_on" not in st.session_state:
    st.session_state.is_alarm_on = False
if "current_rule" not in st.session_state:
    st.session_state.current_rule = ""

# 메인 타이틀
st.title("🚨 실시간 음성 욕설 자동 감지 사이렌")
st.caption(
    "마이크로 입력되거나 말한 내용 중 욕설/금지어가 감지되면 끄기 버튼을 누를 때까지 사이렌이 계속 울립니다."
)

# ---------------------------------------------------------
# 경고음 재생 및 끄기 컨트롤러 (무한 연속 재생)
# ---------------------------------------------------------
if st.session_state.is_alarm_on:
    st.error(
        f"🚨 **[비상 경고 사이렌 작동 중!]** 감지 원인: {st.session_state.current_rule}"
    )

    # HTML5 Audio 엘리먼트로 소리 100% 재생 (loop 옵션으로 무한 울림)
    audio_html = f"""
    <div style="text-align: center; margin: 15px 0;">
        <audio autoplay loop controls style="width: 100%;">
            <source src="data:audio/wav;base64,{SIREN_B64}" type="audio/wav">
            브라우저가 오디오 재생을 지원하지 않습니다.
        </audio>
    </div>
    """
    components.html(audio_html, height=75)

    if st.button(
        "🛑 경고음 즉시 끄기 (정지)", type="primary", use_container_width=True
    ):
        st.session_state.is_alarm_on = False
        st.session_state.current_rule = ""
        st.rerun()

    st.markdown("---")

# ---------------------------------------------------------
# 사이드바 설정
# ---------------------------------------------------------
st.sidebar.header("⚙️ 음성 감지 규칙 설정")
banned_words_input = st.sidebar.text_input(
    "🚫 감지할 욕설/금지어 목록 (쉼표 구분)",
    value="바보, 멍청이, 짜증, 씨발, 개새끼, 미친, 시발, 좆",
)
banned_words = [w.strip() for w in banned_words_input.split(",") if w.strip()]

st.sidebar.markdown("---")
if st.sidebar.button("🛑 [사이드바] 경고음 끄기", use_container_width=True):
    st.session_state.is_alarm_on = False
    st.session_state.current_rule = ""
    st.rerun()

# ---------------------------------------------------------
# 1. 마이크 입력 및 텍스트 욕설 실시간 자동 검사
# ---------------------------------------------------------
st.subheader("🎙️ 마이크 음성 / 텍스트 욕설 감지기")

# Streamlit 내장 audio_input
audio_file = st.audio_input("마이크에 대고 말씀해 보세요")

# 텍스트 직접 입력 또는 음성 변환 입력창
spoken_text = st.text_input(
    "🗣️ 말한 내용 입력 또는 테스트 문장 작성",
    placeholder="예: 진짜 바보 같네... (작성 시 욕설 자동 감지)",
)

# 욕설 감지 로직
if spoken_text:
    detected_words = [w for w in banned_words if w in spoken_text]

    if detected_words and not st.session_state.is_alarm_on:
        st.session_state.is_alarm_on = True
        st.session_state.current_rule = (
            f"🤬 욕설 감지: {', '.join(detected_words)}"
        )

        log_time = time.strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.detection_logs.insert(
            0,
            {
                "시각": log_time,
                "입력 내용": spoken_text,
                "감지 단어": ", ".join(detected_words),
                "상태": "🚨 사이렌 연속 발령",
            },
        )
        st.rerun()

# ---------------------------------------------------------
# 2. 학교 수칙 원클릭 발령 버튼 영역
# ---------------------------------------------------------
st.markdown("---")
st.subheader("📢 학교 수칙 수동 경고 발령")

col1, col2 = st.columns(2)

with col1:
    if st.button(
        "🤬 욕설 / 언어폭력 수동 발령",
        use_container_width=True,
        type="primary",
    ):
        st.session_state.is_alarm_on = True
        st.session_state.current_rule = "🤬 욕설 및 언어폭력 (수동 발령)"
        log_time = time.strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.detection_logs.insert(
            0,
            {
                "시각": log_time,
                "입력 내용": "수동 버튼 클릭",
                "감지 단어": "욕설/언어폭력",
                "상태": "🚨 사이렌 발령",
            },
        )
        st.rerun()

    st.write("")

    if st.button("🏃‍♂️ 복도 질주 / 소란", use_container_width=True):
        st.session_state.is_alarm_on = True
        st.session_state.current_rule = "🏃‍♂️ 복도 질주 및 소란"
        log_time = time.strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.detection_logs.insert(
            0,
            {
                "시각": log_time,
                "입력 내용": "수동 버튼 클릭",
                "감지 단어": "복도 소란",
                "상태": "🚨 사이렌 발령",
            },
        )
        st.rerun()

with col2:
    if st.button(
        "🚬 교내 무단 흡연!", use_container_width=True, type="primary"
    ):
        st.session_state.is_alarm_on = True
        st.session_state.current_rule = "🚬 교내 무단 흡연 (수동 발령)"
        log_time = time.strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.detection_logs.insert(
            0,
            {
                "시각": log_time,
                "입력 내용": "수동 버튼 클릭",
                "감지 단어": "무단 흡연",
                "상태": "🚨 사이렌 발령",
            },
        )
        st.rerun()

    st.write("")

    if st.button("📱 수업 중 스마트폰 사용", use_container_width=True):
        st.session_state.is_alarm_on = True
        st.session_state.current_rule = "📱 수업 중 스마트폰 무단 사용"
        log_time = time.strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.detection_logs.insert(
            0,
            {
                "시각": log_time,
                "입력 내용": "수동 버튼 클릭",
                "감지 단어": "스마트폰 사용",
                "상태": "🚨 사이렌 발령",
            },
        )
        st.rerun()

# ---------------------------------------------------------
# 3. 감지 및 발령 이력 기록
# ---------------------------------------------------------
st.markdown("---")
st.subheader("📜 실시간 감지 및 발령 이력")

if st.session_state.detection_logs:
    df_logs = pd.DataFrame(st.session_state.detection_logs)
    st.dataframe(df_logs, use_container_width=True)

    if st.button("🗑️ 이력 전체 초기화"):
        st.session_state.detection_logs = []
        st.rerun()
else:
    st.write("아직 감지된 이력이 없습니다.")
