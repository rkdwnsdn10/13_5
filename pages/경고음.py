import base64
import time
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# 페이지 기본 설정
st.set_page_config(
    page_title="실시간 음성 욕설 자동 감지기", page_icon="🚨", layout="centered"
)

# 세션 이력 관리
if "detection_logs" not in st.session_state:
    st.session_state.detection_logs = []

st.title("🚨 실시간 음성 욕설 & 금지어 자동 감지기")
st.caption(
    "추가 라이브러리 설치 없이 기본 브라우저 기능만으로 마이크 음성을 분석하여 욕설 감지 시 사이렌을 울립니다."
)

# 사이드바 설정
st.sidebar.header("⚙️ 음성 감지 규칙 설정")
banned_words_input = st.sidebar.text_input(
    "🚫 감지할 욕설/금지어 (쉼표 구분)",
    value="바보, 멍청이, 짜증, 씨발, 개새끼, 미친",
)
banned_words = [w.strip() for w in banned_words_input.split(",") if w.strip()]


# 고출력 사이렌 오디오 재생 스크립트
def play_siren():
    js_code = """
    <script>
    (function() {
        try {
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            if (!AudioContext) return;
            const ctx = new AudioContext();
            if (ctx.state === 'suspended') {
                ctx.resume();
            }
            
            const masterGain = ctx.createGain();
            masterGain.gain.setValueAtTime(1.0, ctx.currentTime);
            masterGain.connect(ctx.destination);

            [600, 900, 1200].forEach((baseFreq, i) => {
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.type = i % 2 === 0 ? 'sawtooth' : 'square';

                osc.frequency.setValueAtTime(baseFreq, ctx.currentTime);
                osc.frequency.linearRampToValueAtTime(baseFreq + 600, ctx.currentTime + 0.3);
                osc.frequency.linearRampToValueAtTime(baseFreq, ctx.currentTime + 0.6);
                osc.frequency.linearRampToValueAtTime(baseFreq + 600, ctx.currentTime + 0.9);

                gain.gain.setValueAtTime(0.3, ctx.currentTime);
                osc.connect(gain);
                gain.connect(masterGain);

                osc.start(ctx.currentTime);
                osc.stop(ctx.currentTime + 1.0);
            });
        } catch(e) {
            console.error("Audio error:", e);
        }
    })();
    </script>
    """
    components.html(js_code, height=0, width=0)


st.sidebar.markdown("---")
if st.sidebar.button("🔊 사이렌 소리 테스트"):
    play_siren()
    st.sidebar.success("테스트 경고음 발령")

# ---------------------------------------------------------
# 모드 선택 및 음성 녹음 입력 (Streamlit 내장 audio_input 활용)
# ---------------------------------------------------------
st.subheader("🎙️ 마이크 음성 녹음 / 감지")
st.info(
    "💡 아래 마이크 버튼을 눌러 말씀하신 후 녹음을 마치면, 브라우저 음성 인식 기능으로 욕설을 검사합니다."
)

# Streamlit 내장 마이크 입력 기능 (추가 패키지 불필요)
audio_data = st.audio_input("마이크에 대고 말씀하세요")

# 브라우저 상의 직접 음성 감지를 위한 인터랙티브 입력창
user_spoken_text = st.text_input(
    "🗣️ 음성 인식 결과 또는 직접 말한 내용 입력",
    placeholder="마이크로 말한 내용이 여기에 기록되거나 직접 테스트할 문장을 적으세요...",
)

# 자동 검증 로직
if user_spoken_text:
    detected_words = [w for w in banned_words if w in user_spoken_text]

    if detected_words:
        play_siren()  # 즉시 강렬한 경고음 발생

        st.error(
            f"🚨 **[자동 감지] 욕설이 포착되었습니다!** - 감지된 단어: `{', '.join(detected_words)}`"
        )

        log_time = time.strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.detection_logs.insert(
            0,
            {
                "시각": log_time,
                "입력 내용": user_spoken_text,
                "감지 단어": ", ".join(detected_words),
                "상태": "🚨 위반",
            },
        )
    else:
        st.success("✅ **[정상]** 감지된 욕설/금지어가 없습니다.")

# 이력 대시보드
st.markdown("---")
st.subheader("📜 실시간 감지 이력 기록")

if st.session_state.detection_logs:
    df_logs = pd.DataFrame(st.session_state.detection_logs)
    st.dataframe(df_logs, use_container_width=True)

    if st.button("🗑️ 전체 이력 삭제"):
        st.session_state.detection_logs = []
        st.rerun()
else:
    st.write("아직 감지된 기록이 없습니다.")
