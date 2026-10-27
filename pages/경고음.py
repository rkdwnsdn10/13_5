import io
import re
import struct
import time
import wave
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# 페이지 기본 설정
st.set_page_config(
    page_title="5대 생활 수칙 실시간 자동 감지기",
    page_icon="🚨",
    layout="centered",
)


# ---------------------------------------------------------
# 1. WAV 음원 생성기 (파이썬 내장 wave 모듈 활용 - 외부 라이브러리 0개)
# ---------------------------------------------------------
def create_siren_wav(sound_type="siren"):
    """브라우저에 확실히 전달되는 WAV 오디오 바이너리 생성"""
    sample_rate = 22050
    duration = 0.8 if sound_type == "siren" else 0.4
    num_samples = int(sample_rate * duration)

    buf = io.BytesIO()
    with wave.open(buf, "wb") as wav_file:
        wav_file.setnchannels(1)  # 모노
        wav_file.setsampwidth(2)  # 16비트
        wav_file.setframerate(sample_rate)

        frames = []
        for i in range(num_samples):
            t = i / sample_rate
            if sound_type == "siren":
                # 피치가 오르락내리락하는 비상 사이렌 (500Hz ~ 1200Hz)
                freq = 500 + 700 * (0.5 + 0.5 * (1 if (int(t * 8) % 2) else -1))
            elif sound_type == "cleaning":
                # 청소 독촉 880Hz 비프
                freq = 880 if (int(t * 10) % 2 == 0) else 0
            elif sound_type == "noise":
                # 층간소음 경고 1000Hz -> 300Hz 하강음
                freq = max(300, 1000 - (t * 1200))
            else:
                # 일반 750Hz 비프
                freq = 750

            # 파형 생성
            if freq > 0:
                val = int(
                    32767.0 * 0.5 * (1 if (t * freq * 2) % 2 < 1 else -1)
                )  # Square wave
            else:
                val = 0
            frames.append(struct.pack("<h", val))

        wav_file.writeframes(b"".join(frames))

    return buf.getvalue()


# ---------------------------------------------------------
# 2. Web Audio API 강제 활성화 스크립트 (차단 우회)
# ---------------------------------------------------------
def play_web_audio_alarm(sound_type="siren"):
    js_code = f"""
    <script>
    (function() {{
        try {{
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            if (!AudioContext) return;
            
            // 기존 멈춤 상태 강제 깨우기 (resume)
            let ctx = window._globalAudioCtx;
            if (!ctx) {{
                ctx = new AudioContext();
                window._globalAudioCtx = ctx;
            }}
            if (ctx.state === 'suspended') {{
                ctx.resume();
            }}
            
            const type = "{sound_type}";
            const masterGain = ctx.createGain();
            masterGain.gain.setValueAtTime(0.8, ctx.currentTime);
            masterGain.connect(ctx.destination);
            
            if (type === "siren") {{
                const osc = ctx.createOscillator();
                osc.type = 'sawtooth';
                osc.frequency.setValueAtTime(600, ctx.currentTime);
                osc.frequency.linearRampToValueAtTime(1200, ctx.currentTime + 0.3);
                osc.frequency.linearRampToValueAtTime(600, ctx.currentTime + 0.6);
                osc.connect(masterGain);
                osc.start(ctx.currentTime);
                osc.stop(ctx.currentTime + 0.7);
            }} else {{
                const osc = ctx.createOscillator();
                osc.type = 'square';
                osc.frequency.setValueAtTime(800, ctx.currentTime);
                osc.connect(masterGain);
                osc.start(ctx.currentTime);
                osc.stop(ctx.currentTime + 0.3);
            }}
        }} catch(e) {{
            console.error(e);
        }}
    }})();
    </script>
    """
    components.html(js_code, height=0, width=0)


# 세션 관리
if "detection_logs" not in st.session_state:
    st.session_state.detection_logs = []
if "play_sound_trigger" not in st.session_state:
    st.session_state.play_sound_trigger = None

# 메인 UI
st.title("🚨 5대 생활 수칙 실시간 자동 감지기")
st.caption("위반 사항 감지 시 크고 강렬한 경고음이 즉시 출력됩니다.")

# 브라우저 차단 해제 클릭 유도 버튼
st.warning(
    "⚠️ **소리가 안 날 때 해결법**: 아래 [🔊 브라우저 사운드 차단 해제] 버튼을 1회 누르시면 소리가 정상 출력됩니다!"
)
if st.button("🔊 브라우저 사운드 차단 해제 (필수 클릭)", type="secondary"):
    play_web_audio_alarm("siren")
    st.success("브라우저 오디오 오디오 권한이 승인되었습니다!")

# 사이드바 설정
st.sidebar.header("⚙️ 세부 검증 규칙 설정")
banned_input = st.sidebar.text_input(
    "1️⃣ 금지어/비속어 목록", value="욕설, 바보, 짜증, 나쁜말"
)
cleaning_input = st.sidebar.text_input(
    "2️⃣ 청소/정리 미이행 목록", value="청소 안함, 쓰레기, 설거지"
)
noise_input = st.sidebar.text_input(
    "3️⃣ 소음/층간소음 목록", value="뛰어다님, 고성방가, 시끄러움"
)
smoking_input = st.sidebar.text_input(
    "4️⃣ 실내 흡연 관련 목록", value="담배, 흡연, 전자담배"
)
max_chars = st.sidebar.number_input(
    "5️⃣ 최대 허용 글자 수", min_value=10, max_value=500, value=150
)

banned_words = [w.strip() for w in banned_input.split(",") if w.strip()]
cleaning_words = [w.strip() for w in cleaning_input.split(",") if w.strip()]
noise_words = [w.strip() for w in noise_input.split(",") if w.strip()]
smoking_words = [w.strip() for w in smoking_input.split(",") if w.strip()]

# 검증 영역
st.subheader("📝 현재 상황 / 작성 내용 입력")
user_text = st.text_area(
    "상황을 입력하면 규칙 위반을 자동 판별합니다:",
    placeholder="예: 거실에서 담배 피우고 청소도 안 했어...",
    height=120,
)

if st.button("🔍 5대 규칙 위반 자동 검사", type="primary"):
    if not user_text.strip():
        st.warning("검사할 내용을 입력해 주세요.")
    else:
        violations = []
        sound_type = None

        if any(w in user_text for w in smoking_words):
            violations.append("🚬 **[규칙 4 위반] 실내 흡연 감지**")
            sound_type = "siren"
        elif any(w in user_text for w in banned_words):
            violations.append("🤬 **[규칙 1 위반] 비속어/금지어 감지**")
            sound_type = "siren"
        elif any(w in user_text for w in cleaning_words):
            violations.append("🧹 **[규칙 2 위반] 청소 미이행 감지**")
            sound_type = "cleaning"
        elif any(w in user_text for w in noise_words):
            violations.append("🔊 **[규칙 3 위반] 소음 감지**")
            sound_type = "noise"
        elif len(user_text) > max_chars:
            violations.append("📏 **[규칙 5 위반] 글자 수 초과**")
            sound_type = "beep"

        if violations:
            st.session_state.play_sound_trigger = sound_type
            for v in violations:
                st.error(v)
                st.session_state.detection_logs.insert(
                    0,
                    {
                        "시각": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "위반": v,
                    },
                )
        else:
            st.session_state.play_sound_trigger = None
            st.success("✅ **[정상]** 규칙 위반 사항이 없습니다.")

# 음원 재생 처리 (2중 보장)
if st.session_state.play_sound_trigger:
    s_type = st.session_state.play_sound_trigger

    # 방법 1: Web Audio 스크립트 실행
    play_web_audio_alarm(s_type)

    # 방법 2: Streamlit 내장 플레이어 자동 재생 (가장 확실함)
    wav_bytes = create_siren_wav(s_type)
    st.audio(wav_bytes, format="audio/wav", autoplay=True)

    # 트리거 리셋
    st.session_state.play_sound_trigger = None

# 이력 출력
st.markdown("---")
st.subheader("📜 위반 감지 이력")
if st.session_state.detection_logs:
    st.dataframe(
        pd.DataFrame(st.session_state.detection_logs), use_container_width=True
    )
