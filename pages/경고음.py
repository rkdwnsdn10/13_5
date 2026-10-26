import base64
import time
import google.generativeai as genai
import numpy as np
from PIL import Image
import streamlit as st
import streamlit.components.v1 as components

# 페이지 기본 설정
st.set_page_config(
    page_title="AI 실시간 규칙 위반 자동 감지기", page_icon="🚨", layout="centered"
)


# 고출력 증폭 경고음 발생 스크립트 (Web Audio API Gain Node 증폭)
def play_loud_siren():
    js_code = """
    <script>
    (function() {
        try {
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            if (!AudioContext) return;
            const ctx = new AudioContext();
            
            // 3중 오실레이터 + Gain 증폭기 조합으로 극대화된 사이렌 소리 생성
            const masterGain = ctx.createGain();
            masterGain.gain.setValueAtTime(0.9, ctx.currentTime); // 고출력 볼륨
            masterGain.connect(ctx.destination);
            
            const frequencies = [600, 900, 1200];
            frequencies.forEach((baseFreq, i) => {
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.type = i % 2 === 0 ? 'sawtooth' : 'square'; // 강렬한 파형
                
                // 사이렌 피치 변조 (Siren Sweep)
                osc.frequency.setValueAtTime(baseFreq, ctx.currentTime);
                osc.frequency.linearRampToValueAtTime(baseFreq + 500, ctx.currentTime + 0.3);
                osc.frequency.linearRampToValueAtTime(baseFreq, ctx.currentTime + 0.6);
                osc.frequency.linearRampToValueAtTime(baseFreq + 500, ctx.currentTime + 0.9);
                
                gain.gain.setValueAtTime(0.3, ctx.currentTime);
                osc.connect(gain);
                gain.connect(masterGain);
                
                osc.start(ctx.currentTime);
                osc.stop(ctx.currentTime + 1.0);
            });
        } catch(e) {
            console.error("Audio playback error:", e);
        }
    })();
    </script>
    """
    components.html(js_code, height=0, width=0)


# Gemini API 키 확인 및 초기화
api_key = st.secrets.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# 세션 상태 초기화
if "detection_logs" not in st.session_state:
    st.session_state.detection_logs = []

# 앱 타이틀
st.title("🚨 실시간 규칙 위반 자동 감지 시스템")
st.caption("카메라와 마이크 분석을 통해 위반 사항 감지 시 크고 강렬한 경고음이 자동 발령됩니다.")

st.info("💡 **시작하기 전**: 브라우저 오디오 권한을 위해 화면 아무 곳이나 1회 클릭해 주세요.")

# 사이드바 설정
st.sidebar.header("⚙️ 자동 감지 규칙 설정")

detection_mode = st.sidebar.radio(
    "감지 모드 선택",
    ["📹 웹캠 행동/상태 AI 자동 감지", "🎙️ 마이크 소음/고성 자동 감지"],
)

st.sidebar.markdown("---")
st.sidebar.subheader("🔊 경고음 볼륨 및 음량 테스트")
if st.sidebar.button("🔊 고출력 사이렌 테스트"):
    play_loud_siren()
    st.sidebar.success("강렬한 사이렌 경고음 출력 테스트")

# ---------------------------------------------------------
# 모드 1: 웹캠 + Gemini AI 행동/상태 자동 감지
# ---------------------------------------------------------
if detection_mode == "📹 웹캠 행동/상태 AI 자동 감지":
    st.subheader("📹 웹캠 AI 위반 감지 모드")

    if not api_key:
        st.error(
            "⚠️ Streamlit Secrets에 `GEMINI_API_KEY`가 설정되어 있지 않습니다."
        )
        st.stop()

    rule_description = st.text_input(
        "감지할 위반 규칙 설정 (자연어로 작성)",
        value="청소를 안 하고 쓰레기가 방치된 상태, 손가락으로 욕설을 하는 행위, 실내 흡연",
    )

    img_file = st.camera_input("카메라로 실시간 위반 상태 촬영 / 자동 스캔")

    if img_file:
        image = Image.open(img_file)
        st.image(image, caption="스캔된 프레임", width=350)

        with st.spinner("AI가 규칙 위반 여부를 검석하고 있습니다..."):
            try:
                model = genai.GenerativeModel("gemini-2.5-flash-lite")
                prompt = f"""
                당신은 실시간 안전 및 규칙 모니터링 AI입니다.
                다음 [위반 규칙 목록]에 해당하는 행동이나 상태가 이미지에 포함되어 있는지 판단하세요.
                
                [위반 규칙 목록]: {rule_description}
                
                응답 형식:
                첫 번째 줄에는 반드시 'VIOLATION' 또는 'NORMAL' 중 하나만 작성하세요.
                두 번째 줄에는 판단 이유를 한 문장으로 간단히 설명하세요.
                """

                response = model.generate_content([prompt, image])
                result_text = response.text.strip()

                lines = result_text.split("\n")
                status = lines[0].strip().upper()
                reason = lines[1] if len(lines) > 1 else result_text

                if "VIOLATION" in status:
                    # 크고 강렬한 경고음 자동 재생
                    play_loud_siren()

                    st.error(f"🚨 **[자동 감지] 위반 사항이 포착되었습니다!**")
                    st.write(f"**이유:** {reason}")

                    log_item = f"[{time.strftime('%H:%M:%S')}] 🚨 위반 감지: {reason}"
                    st.session_state.detection_logs.insert(0, log_item)
                else:
                    st.success("✅ **[정상]** 설정된 규칙 위반 사항이 감지되지 않았습니다.")
                    st.write(f"**분석:** {reason}")

            except Exception as e:
                st.error(f"AI 분석 중 오류가 발생했습니다: {str(e)}")

# ---------------------------------------------------------
# 모드 2: 마이크 데시벨/소음 자동 감지
# ---------------------------------------------------------
else:
    st.subheader("🎙️ 마이크 소음 & 고성 자동 감지 모드")

    noise_threshold = st.slider(
        "경고음발생 임계 소음 수치 (기준 데시벨)",
        min_value=30,
        max_value=100,
        value=70,
    )

    audio_file = st.audio_input("마이크로 주변 소음 / 음성을 녹음하여 측정하세요")

    if audio_file:
        try:
            # 음성 파일에서 진폭/데시벨 계산
            audio_bytes = audio_file.read()
            # 간단한 바이너리 진폭 계산
            audio_data = np.frombuffer(audio_bytes, dtype=np.int16)
            if len(audio_data) > 0:
                rms = np.sqrt(np.mean(audio_data**2))
                decibel = int(20 * np.log10(rms)) if rms > 0 else 0
            else:
                decibel = 0

            st.metric("측정된 소음 수치", f"{decibel} dB")

            if decibel >= noise_threshold:
                # 크고 강렬한 경고음 자동 재생
                play_loud_siren()

                st.error(
                    f"🚨 **[소음 초과 감지]** 기준 수치({noise_threshold} dB)를 초과했습니다! ({decibel} dB)"
                )
                log_item = f"[{time.strftime('%H:%M:%S')}] 🚨 소음 초과 감지: {decibel} dB"
                st.session_state.detection_logs.insert(0, log_item)
            else:
                st.success(
                    f"✅ **[정상]** 소음 수치가 허용 범위 내입니다. ({decibel} dB)"
                )

        except Exception as e:
            st.error(f"오디오 분석 중 오류가 발생했습니다: {str(e)}")

# 로그 기록 영역
st.markdown("---")
st.subheader("📜 실시간 자동 감지 이력")

if st.session_state.detection_logs:
    for log in st.session_state.detection_logs[:10]:
        st.write(log)
else:
    st.write("아직 감지된 규칙 위반 기록이 없습니다.")
