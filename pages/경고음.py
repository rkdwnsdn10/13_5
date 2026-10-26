from datetime import datetime
import streamlit as st
import streamlit.components.v1 as components

# 페이지 설정
st.set_page_config(
    page_title="생활 규칙 위반 경고음 사이렌", page_icon="🚨", layout="centered"
)


# Web Audio API 기반 오디오 생성 함수 (100% 오류 없는 브라우저 합성 방식)
def trigger_alert_sound(sound_type):
    js_code = f"""
    <script>
    (function() {{
        try {{
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            if (!AudioContext) return;
            const ctx = new AudioContext();
            const type = "{sound_type}";
            
            if (type === "siren") {{
                // 욕설/언어폭력: 강한 사이렌 경고음
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.type = 'sawtooth';
                gain.gain.setValueAtTime(0.3, ctx.currentTime);
                
                // Frequency Modulation for Siren
                osc.frequency.setValueAtTime(500, ctx.currentTime);
                osc.frequency.linearRampToValueAtTime(1200, ctx.currentTime + 0.25);
                osc.frequency.linearRampToValueAtTime(500, ctx.currentTime + 0.5);
                osc.frequency.linearRampToValueAtTime(1200, ctx.currentTime + 0.75);
                
                osc.connect(gain);
                gain.connect(ctx.destination);
                osc.start(ctx.currentTime);
                osc.stop(ctx.currentTime + 0.8);
            }} else if (type === "cleaning") {{
                // 청소 미이행: 반복 비프음 (독촉)
                [0, 0.15, 0.3].forEach(delay => {{
                    const osc = ctx.createOscillator();
                    const gain = ctx.createGain();
                    osc.type = 'square';
                    osc.frequency.setValueAtTime(900, ctx.currentTime + delay);
                    gain.gain.setValueAtTime(0.25, ctx.currentTime + delay);
                    gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + delay + 0.1);
                    osc.connect(gain);
                    gain.connect(ctx.destination);
                    osc.start(ctx.currentTime + delay);
                    osc.stop(ctx.currentTime + delay + 0.1);
                }});
            }} else if (type === "noise") {{
                // 층간소음/흡연: 하강 트랜지스터 비상음
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.type = 'sine';
                osc.frequency.setValueAtTime(1000, ctx.currentTime);
                osc.frequency.exponentialRampToValueAtTime(200, ctx.currentTime + 0.5);
                gain.gain.setValueAtTime(0.4, ctx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.5);
                osc.connect(gain);
                gain.connect(ctx.destination);
                osc.start(ctx.currentTime);
                osc.stop(ctx.currentTime + 0.5);
            }}
        }} catch(e) {{
            console.error("Audio Playback Error:", e);
        }}
    }})();
    </script>
    """
    components.html(js_code, height=0, width=0)


# 세션 이력 초기화
if "logs" not in st.session_state:
    st.session_state.logs = []

# 메인 타이틀
st.title("🚨 규칙 위반 경고음 사이렌")
st.caption("버튼을 누르면 즉시 해당 위반에 맞는 경고음이 울립니다.")

st.info(
    "💡 **안내**: 웹 브라우저 정책상 화면을 아무 곳이나 **최소 1회 클릭**한 뒤 버튼을 눌러야 오디오가 출력됩니다."
)

st.markdown("---")

# 규칙별 경고 버튼 섹션
st.subheader("📢 위반 상황별 경고 버튼")

col1, col2 = st.columns(2)

with col1:
    # 1. 청소 미이행 버튼
    if st.button(
        "🧹 청소 / 정리 안 함!", use_container_width=True, type="secondary"
    ):
        trigger_alert_sound("cleaning")
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.logs.insert(
            0, f"[{now_str}] 🧹 청소/정리 미이행 경고발생"
        )
        st.warning("🚨 [청소 미이행] 당번은 즉시 정리정돈을 실시하세요!")

    st.write("")

    # 2. 층간소음 / 고성방가 버튼
    if st.button(
        "🔊 층간소음 / 고성방가!", use_container_width=True, type="secondary"
    ):
        trigger_alert_sound("noise")
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.logs.insert(
            0, f"[{now_str}] 🔊 소음 초과 경고발생"
        )
        st.error("🚨 [소음 위반] 주위가 시끄럽습니다! 조용히 해주세요.")

with col2:
    # 3. 욕설 / 비속어 사용 버튼
    if st.button(
        "🤬 욕설 / 비속어 사용!", use_container_width=True, type="primary"
    ):
        trigger_alert_sound("siren")
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.logs.insert(
            0, f"[{now_str}] 🤬 욕설/비속어 사용 경고발생"
        )
        st.error("🚨 [벌칙] 고운 말을 사용합시다! 욕설이 감지되었습니다.")

    st.write("")

    # 4. 무단 흡연 / 기타 위반
    if st.button(
        "🚬 실내 흡연 / 기타 규칙 위반!",
        use_container_width=True,
        type="primary",
    ):
        trigger_alert_sound("siren")
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.logs.insert(
            0, f"[{now_str}] 🚬 실내 흡연/규칙 위반 경고발생"
        )
        st.error("🚨 [경고] 금지된 행동이 감지되었습니다!")

st.markdown("---")

# 최근 위반 기록 이력 출력
st.subheader("📜 최근 경고음 발령 이력")

if st.session_state.logs:
    for log in st.session_state.logs[:10]:  # 최근 10개만 표시
        st.write(log)

    if st.button("🗑️ 이력 전체 삭제"):
        st.session_state.logs = []
        st.rerun()
else:
    st.write("아직 발령된 경고 기록이 없습니다.")
