import time
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# 페이지 기본 설정
st.set_page_config(
    page_title="실시간 규칙 위반 자동 감지기", page_icon="🚨", layout="centered"
)


# 외부 라이브러리 필요 없는 고출력 증폭 사이렌 (Web Audio API)
def play_loud_siren():
    js_code = """
    <script>
    (function() {
        try {
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            if (!AudioContext) return;
            const ctx = new AudioContext();
            
            const masterGain = ctx.createGain();
            masterGain.gain.setValueAtTime(1.0, ctx.currentTime);
            masterGain.connect(ctx.destination);
            
            const frequencies = [600, 900, 1200];
            frequencies.forEach((baseFreq, i) => {
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.type = i % 2 === 0 ? 'sawtooth' : 'square';
                
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


# 세션 상태 초기화
if "detection_logs" not in st.session_state:
    st.session_state.detection_logs = []

# 타이틀
st.title("🚨 실시간 규칙 위반 자동 감지 시스템")
st.caption(
    "설정된 생활 규칙을 위반할 경우 즉시 크고 강렬한 경고음이 자동 발령됩니다."
)

st.info(
    "💡 **안내**: 브라우저 오디오 정책상 화면 아무 곳이나 **1회 이상 클릭**해 주세요."
)

# 사이드바 설정
st.sidebar.header("⚙️ 위반 검증 규칙 설정")

# 금지어 설정
banned_input = st.sidebar.text_input(
    "🚫 감지할 금지어/욕설 목록 (쉼표 구분)",
    value="욕설, 나쁜말, 청소 안함, 소란",
)
banned_words = [w.strip() for w in banned_input.split(",") if w.strip()]

# 글자 수 규칙
max_chars = st.sidebar.number_input(
    "📏 텍스트 최대 허용 글자 수", min_value=10, max_value=500, value=100
)

st.sidebar.markdown("---")
if st.sidebar.button("🔊 고출력 사이렌 소리 테스트"):
    play_loud_siren()
    st.sidebar.success("테스트 경고음 출력 완료")

# 규칙 검증 영역
st.subheader("📝 실시간 행동/상태 규칙 검증")

user_text = st.text_area(
    "현재 상황이나 작성 글을 입력하면 규칙 위반을 자동 판별합니다:",
    placeholder="예: 오늘 청소를 안 하고 나갔어...",
    height=120,
)

if st.button("🚨 규칙 위반 여부 자동 검사", type="primary"):
    if not user_text.strip():
        st.warning("검사할 내용을 입력해 주세요.")
    else:
        violations = []

        # 규칙 1: 금지어/욕설 감지
        detected_banned = [w for w in banned_words if w in user_text]
        if detected_banned:
            violations.append(
                f"금지어/위반 사항 감지: {', '.join(detected_banned)}"
            )

        # 규칙 2: 글자 수 초과 감지
        if len(user_text) > max_chars:
            violations.append(
                f"글자 수 초과 (현재 {len(user_text)}자 / 제한 {max_chars}자)"
            )

        # 위반 시 경고음 발생 및 로그 남기기
        if violations:
            play_loud_siren()  # 즉시 고출력 경고음 발생

            for v in violations:
                st.error(f"🚨 **[자동 감지] 위반 포착!** - {v}")
                log_time = time.strftime("%H:%M:%S")
                st.session_state.detection_logs.insert(
                    0, {"시간": log_time, "위반 내용": v, "상태": "🚨 위반"}
                )
        else:
            st.success("✅ **[정상]** 규칙 위반 사항이 없습니다.")

# 이력 출력 (pandas 활용)
st.markdown("---")
st.subheader("📜 실시간 자동 감지 이력")

if st.session_state.detection_logs:
    df_logs = pd.DataFrame(st.session_state.detection_logs)
    st.dataframe(df_logs, use_container_width=True)

    if st.button("🗑️ 기록 초기화"):
        st.session_state.detection_logs = []
        st.rerun()
else:
    st.write("아직 감지된 규칙 위반 기록이 없습니다.")
