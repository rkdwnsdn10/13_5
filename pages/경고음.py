import time
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# 페이지 기본 설정
st.set_page_config(
    page_title="학교 생활 수칙 위반 경고 사이렌", page_icon="🚨", layout="centered"
)


# 고출력 증폭 경고음 발생 엔진 (Web Audio API)
def play_school_alarm(sound_type="siren"):
    js_code = f"""
    <script>
    (function() {{
        try {{
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            if (!AudioContext) return;
            const ctx = new AudioContext();
            
            if (ctx.state === 'suspended') {{
                ctx.resume();
            }}
            
            const type = "{sound_type}";
            const masterGain = ctx.createGain();
            masterGain.gain.setValueAtTime(1.0, ctx.currentTime);
            masterGain.connect(ctx.destination);
            
            if (type === "siren") {{
                // 강렬한 비상 사이렌 (욕설, 무단 흡연)
                const frequencies = [600, 900, 1200];
                frequencies.forEach((baseFreq, i) => {{
                    const osc = ctx.createOscillator();
                    const gain = ctx.createGain();
                    osc.type = i % 2 === 0 ? 'sawtooth' : 'square';
                    
                    osc.frequency.setValueAtTime(baseFreq, ctx.currentTime);
                    osc.frequency.linearRampToValueAtTime(baseFreq + 600, ctx.currentTime + 0.3);
                    osc.frequency.linearRampToValueAtTime(baseFreq, ctx.currentTime + 0.6);
                    osc.frequency.linearRampToValueAtTime(baseFreq + 600, ctx.currentTime + 0.9);
                    
                    gain.gain.setValueAtTime(0.35, ctx.currentTime);
                    osc.connect(gain);
                    gain.connect(masterGain);
                    
                    osc.start(ctx.currentTime);
                    osc.stop(ctx.currentTime + 1.0);
                }});
            }} else if (type === "noise") {{
                // 복도 질주 및 소란 경고음
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.type = 'sawtooth';
                osc.frequency.setValueAtTime(1200, ctx.currentTime);
                osc.frequency.exponentialRampToValueAtTime(250, ctx.currentTime + 0.6);
                gain.gain.setValueAtTime(0.5, ctx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.6);
                osc.connect(gain);
                gain.connect(masterGain);
                osc.start(ctx.currentTime);
                osc.stop(ctx.currentTime + 0.6);
            }} else if (type === "beep") {{
                // 스마트폰 사용 및 복장 규정 위반 비프음
                [0, 0.15, 0.3].forEach(delay => {{
                    const osc = ctx.createOscillator();
                    const gain = ctx.createGain();
                    osc.type = 'square';
                    osc.frequency.setValueAtTime(880, ctx.currentTime + delay);
                    gain.gain.setValueAtTime(0.3, ctx.currentTime + delay);
                    gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + delay + 0.1);
                    osc.connect(gain);
                    gain.connect(masterGain);
                    osc.start(ctx.currentTime + delay);
                    osc.stop(ctx.currentTime + delay + 0.1);
                }});
            }}
        }} catch(e) {{
            console.error("Audio playback error:", e);
        }}
    }})();
    </script>
    """
    components.html(js_code, height=0, width=0)


# 세션 이력 관리
if "detection_logs" not in st.session_state:
    st.session_state.detection_logs = []

# 메인 타이틀
st.title("🚨 학교 생활 수칙 위반 경고 시스템")
st.caption("원하는 수칙 위반 버튼을 누르면 즉시 맞춤형 경고음이 울립니다.")

st.warning(
    "⚠️ **오디오 안내**: 브라우저 오디오 정책상, 아래 **'🔊 오디오 시스템 활성화'** 버튼을 먼저 1회 누른 후 이용해 주세요!"
)

# 사이드바 오디오 테스트
st.sidebar.header("⚙️ 오디오 시스템")
if st.sidebar.button("🔊 오디오 시스템 활성화 및 소리 테스트"):
    play_school_alarm("siren")
    st.sidebar.success("경고음 오디오 엔진이 준비되었습니다!")

# ---------------------------------------------------------
# 학교 규칙 위반 경고 버튼 영역
# ---------------------------------------------------------
st.subheader("📢 학교 수칙 위반 상황별 원클릭 경고")

col1, col2 = st.columns(2)

with col1:
    # 규칙 1: 욕설 및 언어폭력
    if st.button(
        "🤬 욕설 / 언어폭력 감지!", use_container_width=True, type="primary"
    ):
        play_school_alarm("siren")
        log_time = time.strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.detection_logs.insert(
            0,
            {
                "시각": log_time,
                "위반 수칙": "🤬 욕설 및 언어폭력",
                "경고음": "강렬한 사이렌",
            },
        )
        st.error("🚨 **[규칙 위반]** 바른 말을 사용합시다! 욕설이 적발되었습니다.")

    st.write("")

    # 규칙 2: 복도 무단 질주 / 고성방가
    if st.button(
        "🏃‍♂️ 복도 질주 / 고성방가!",
        use_container_width=True,
        type="secondary",
    ):
        play_school_alarm("noise")
        log_time = time.strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.detection_logs.insert(
            0,
            {
                "시각": log_time,
                "위반 수칙": "🏃‍♂️ 복도 질주 / 소란",
                "경고음": "소음 경고음",
            },
        )
        st.warning(
            "🚨 **[규칙 위반]** 복도에서는 뛰지 말고 우측통행하며 조용히 이동하세요!"
        )

    st.write("")

    # 규칙 3: 수업 중 스마트폰 무단 사용
    if st.button(
        "📱 수업 중 스마트폰 무단 사용!",
        use_container_width=True,
        type="secondary",
    ):
        play_school_alarm("beep")
        log_time = time.strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.detection_logs.insert(
            0,
            {
                "시각": log_time,
                "위반 수칙": "📱 수업 중 스마트폰 사용",
                "경고음": "비프 알림음",
            },
        )
        st.warning(
            "🚨 **[규칙 위반]** 수업 시간에 휴대폰/스마트기기 사용은 금지됩니다!"
        )

with col2:
    # 규칙 4: 교내 무단 흡연 / 전자담배
    if st.button(
        "🚬 교내 무단 흡연 / 전자담배!",
        use_container_width=True,
        type="primary",
    ):
        play_school_alarm("siren")
        log_time = time.strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.detection_logs.insert(
            0,
            {
                "시각": log_time,
                "위반 수칙": "🚬 교내 무단 흡연",
                "경고음": "화재/비상 사이렌",
            },
        )
        st.error(
            "🚨 **[중대 위반]** 학교 전체는 금연구역입니다! 즉시 중단하세요."
        )

    st.write("")

    # 규칙 5: 복장 / 교복 규정 위반
    if st.button(
        "👔 교복 / 용의 복장 미흡!",
        use_container_width=True,
        type="secondary",
    ):
        play_school_alarm("beep")
        log_time = time.strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.detection_logs.insert(
            0,
            {
                "시각": log_time,
                "위반 수칙": "👔 용의 복장 규정 위반",
                "경고음": "비프 알림음",
            },
        )
        st.info("🚨 **[규칙 위반]** 규정에 맞는 단정한 복장을 갖춰주세요.")

    st.write("")

    # 규칙 6: 기타 학교 규칙 위반
    if st.button(
        "⚠️ 기타 학교 규칙 위반!",
        use_container_width=True,
        type="secondary",
    ):
        play_school_alarm("noise")
        log_time = time.strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.detection_logs.insert(
            0,
            {
                "시각": log_time,
                "위반 수칙": "⚠️ 기타 수칙 위반",
                "경고음": "경고음",
            },
        )
        st.error("🚨 **[경고]** 교내 수칙 위반 행동이 감지되었습니다.")

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
