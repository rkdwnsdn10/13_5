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


# 무한 반복 경고음 제어 자바스크립트 엔진 (Web Audio API)
def control_alarm_sound(action="start", sound_type="siren"):
    js_code = f"""
    <script>
    (function() {{
        try {{
            if (!window.alarmAudioCtx) {{
                const AudioContext = window.AudioContext || window.webkitAudioContext;
                if (AudioContext) {{
                    window.alarmAudioCtx = new AudioContext();
                }}
            }}
            
            const ctx = window.alarmAudioCtx;
            if (!ctx) return;
            
            if (window.alarmInterval) {{
                clearInterval(window.alarmInterval);
                window.alarmInterval = null;
            }}
            
            if (ctx.state === 'suspended') {{
                ctx.resume();
            }}

            const action = "{action}";
            const type = "{sound_type}";
            
            if (action === "stop") {{
                ctx.suspend();
                return;
            }}

            function playSingleLoop() {{
                if (ctx.state === 'suspended') ctx.resume();
                
                const masterGain = ctx.createGain();
                masterGain.gain.setValueAtTime(1.0, ctx.currentTime);
                masterGain.connect(ctx.destination);
                
                if (type === "siren") {{
                    const freqs = [600, 900, 1200];
                    freqs.forEach((baseFreq, i) => {{
                        const osc = ctx.createOscillator();
                        const gain = ctx.createGain();
                        osc.type = (i % 2 === 0) ? 'sawtooth' : 'square';
                        
                        osc.frequency.setValueAtTime(baseFreq, ctx.currentTime);
                        osc.frequency.linearRampToValueAtTime(baseFreq + 600, ctx.currentTime + 0.3);
                        osc.frequency.linearRampToValueAtTime(baseFreq, ctx.currentTime + 0.6);
                        osc.frequency.linearRampToValueAtTime(baseFreq + 600, ctx.currentTime + 0.9);
                        
                        gain.gain.setValueAtTime(0.35, ctx.currentTime);
                        osc.connect(gain);
                        gain.connect(masterGain);
                        
                        osc.start(ctx.currentTime);
                        osc.stop(ctx.currentTime + 0.95);
                    }});
                }} else if (type === "noise") {{
                    const osc = ctx.createOscillator();
                    const gain = ctx.createGain();
                    osc.type = 'sawtooth';
                    osc.frequency.setValueAtTime(1200, ctx.currentTime);
                    osc.frequency.exponentialRampToValueAtTime(250, ctx.currentTime + 0.5);
                    gain.gain.setValueAtTime(0.5, ctx.currentTime);
                    gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.5);
                    osc.connect(gain);
                    gain.connect(masterGain);
                    osc.start(ctx.currentTime);
                    osc.stop(ctx.currentTime + 0.5);
                }} else if (type === "beep") {{
                    const delays = [0, 0.2, 0.4];
                    delays.forEach(delay => {{
                        const osc = ctx.createOscillator();
                        const gain = ctx.createGain();
                        osc.type = 'square';
                        osc.frequency.setValueAtTime(880, ctx.currentTime + delay);
                        gain.gain.setValueAtTime(0.3, ctx.currentTime + delay);
                        gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + delay + 0.12);
                        osc.connect(gain);
                        gain.connect(masterGain);
                        osc.start(ctx.currentTime);
                        osc.stop(ctx.currentTime + 0.12);
                    }});
                }}
            }}

            playSingleLoop();
            window.alarmInterval = setInterval(playSingleLoop, 1000);
            
        }} catch(e) {{
            console.error("Audio playback error:", e);
        }}
    }})();
    </script>
    """
    components.html(js_code, height=0, width=0)


# 세션 상태 관리
if "detection_logs" not in st.session_state:
    st.session_state.detection_logs = []
if "is_alarm_on" not in st.session_state:
    st.session_state.is_alarm_on = False
if "current_rule" not in st.session_state:
    st.session_state.current_rule = ""

# 메인 타이틀
st.title("🚨 학교 생활 수칙 연속 경고 사이렌")
st.caption(
    "버튼을 누르면 정지할 때까지 경고음이 멈추지 않고 계속 울립니다."
)

st.warning(
    "⚠️ **오디오 시작 안내**: 브라우저 오디오 정책상, 아래 **'🔊 오디오 시스템 활성화'** 버튼을 먼저 1회 눌러주세요."
)

# 사이드바 설정
st.sidebar.header("⚙️ 경고음 제어판")

if st.sidebar.button("🔊 오디오 시스템 활성화"):
    control_alarm_sound("stop")
    st.sidebar.success("경고음 오디오 엔진 준비 완료")

st.sidebar.markdown("---")
# 어디서나 끌 수 있는 사이드바 끄기 버튼
if st.sidebar.button(
    "🛑 [사이드바] 경고음 끄기 (정지)", use_container_width=True
):
    control_alarm_sound("stop")
    st.session_state.is_alarm_on = False
    st.session_state.current_rule = ""
    st.rerun()

# ---------------------------------------------------------
# 경고음 상태 제어 폼
# ---------------------------------------------------------
if st.session_state.is_alarm_on:
    st.error(
        f"🚨 **경고음이 계속 재생 중입니다!** (위반 수칙: {st.session_state.current_rule})"
    )
    if st.button(
        "🛑 경고음 즉시 끄기 (정지)",
        type="primary",
        use_container_width=True,
    ):
        control_alarm_sound("stop")
        st.session_state.is_alarm_on = False
        st.session_state.current_rule = ""
        st.rerun()
    st.markdown("---")

# ---------------------------------------------------------
# 학교 규칙 위반 경고 버튼 영역
# ---------------------------------------------------------
st.subheader("📢 학교 수칙 위반 원클릭 연속 경고")

col1, col2 = st.columns(2)

with col1:
    # 규칙 1: 욕설 및 비속어
    if st.button(
        "🤬 욕설 / 언어폭력 감지!", use_container_width=True, type="primary"
    ):
        control_alarm_sound("start", "siren")
        st.session_state.is_alarm_on = True
        st.session_state.current_rule = "🤬 욕설 및 언어폭력"

        log_time = time.strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.detection_logs.insert(
            0,
            {
                "시각": log_time,
                "위반 수칙": "🤬 욕설 및 언어폭력",
                "경고음": "연속 비상 사이렌",
            },
        )
        st.rerun()

    st.write("")

    # 규칙 2: 복도 무단 질주 / 고성방가
    if st.button(
        "🏃‍♂️ 복도 질주 / 고성방가!",
        use_container_width=True,
        type="secondary",
    ):
        control_alarm_sound("start", "noise")
        st.session_state.is_alarm_on = True
        st.session_state.current_rule = "🏃‍♂️ 복도 질주 / 소란"

        log_time = time.strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.detection_logs.insert(
            0,
            {
                "시각": log_time,
                "위반 수칙": "🏃‍♂️ 복도 질주 / 소란",
                "경고음": "연속 소음 경고음",
            },
        )
        st.rerun()

    st.write("")

    # 규칙 3: 수업 중 스마트폰 무단 사용
    if st.button(
        "📱 수업 중 스마트폰 무단 사용!",
        use_container_width=True,
        type="secondary",
    ):
        control_alarm_sound("start", "beep")
        st.session_state.is_alarm_on = True
        st.session_state.current_rule = "📱 수업 중 스마트폰 사용"

        log_time = time.strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.detection_logs.insert(
            0,
            {
                "시각": log_time,
                "위반 수칙": "📱 수업 중 스마트폰 사용",
                "경고음": "연속 비프 알림음",
            },
        )
        st.rerun()

with col2:
    # 규칙 4: 교내 무단 흡연 / 전자담배
    if st.button(
        "🚬 교내 무단 흡연 / 전자담배!",
        use_container_width=True,
        type="primary",
    ):
        control_alarm_sound("start", "siren")
        st.session_state.is_alarm_on = True
        st.session_state.current_rule = "🚬 교내 무단 흡연"

        log_time = time.strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.detection_logs.insert(
            0,
            {
                "시각": log_time,
                "위반 수칙": "🚬 교내 무단 흡연",
                "경고음": "연속 비상 사이렌",
            },
        )
        st.rerun()

    st.write("")

    # 규칙 5: 복장 / 교복 규정 위반
    if st.button(
        "👔 교복 / 용의 복장 미흡!",
        use_container_width=True,
        type="secondary",
    ):
        control_alarm_sound("start", "beep")
        st.session_state.is_alarm_on = True
        st.session_state.current_rule = "👔 용의 복장 규정 위반"

        log_time = time.strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.detection_logs.insert(
            0,
            {
                "시각": log_time,
                "위반 수칙": "👔 용의 복장 규정 위반",
                "경고음": "연속 비프 알림음",
            },
        )
        st.rerun()

    st.write("")

    # 규칙 6: 기타 학교 규칙 위반
    if st.button(
        "⚠️ 기타 학교 규칙 위반!",
        use_container_width=True,
        type="secondary",
    ):
        control_alarm_sound("start", "noise")
        st.session_state.is_alarm_on = True
        st.session_state.current_rule = "⚠️ 기타 수칙 위반"

        log_time = time.strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.detection_logs.insert(
            0,
            {
                "시각": log_time,
                "위반 수칙": "⚠️ 기타 수칙 위반",
                "경고음": "연속 경고음",
            },
        )
        st.rerun()

# ---------------------------------------------------------
# 위반 이력 대시보드 (Pandas 활용)
# ---------------------------------------------------------
st.markdown("---")
st.subheader("📜 실시간 경고음 발령 이력 기록")

if st.session_state.detection_logs:
    df_logs = pd.DataFrame(st.session_state.detection_logs)
    st.dataframe(df_logs, use_container_width=True)

    if st.button("🗑️ 이력 전체 초기화"):
        st.session_state.detection_logs = []
        st.rerun()
else:
    st.write("아직 발령된 위반 기록이 없습니다.")
