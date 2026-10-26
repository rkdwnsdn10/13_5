import re
import streamlit as st
import streamlit.components.v1 as components

# 페이지 설정
st.set_page_config(
    page_title="실시간 규칙 위반 감지 & 경고음 시스템",
    page_icon="🚨",
    layout="centered"
)


# Web Audio API 기반 오디오 생성 함수 (Streamlit Cloud 호환 100%)
def play_sound(sound_type="beep"):
    """브라우저 단에서 오디오를 합성하여 경고음을 재생하는 스크립트"""
    js_code = f"""
    <script>
    (function() {{
        try {{
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            if (!AudioContext) return;
            const ctx = new AudioContext();
            const type = "{sound_type}";
            
            if (type === "siren") {{
                // 강한 사이렌 경고음 (금지어 위반)
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.type = 'sawtooth';
                gain.gain.setValueAtTime(0.2, ctx.currentTime);
                
                osc.frequency.setValueAtTime(400, ctx.currentTime);
                osc.frequency.linearRampToValueAtTime(900, ctx.currentTime + 0.2);
                osc.frequency.linearRampToValueAtTime(400, ctx.currentTime + 0.4);
                osc.frequency.linearRampToValueAtTime(900, ctx.currentTime + 0.6);
                
                osc.connect(gain);
                gain.connect(ctx.destination);
                osc.start(ctx.currentTime);
                osc.stop(ctx.currentTime + 0.7);
            }} else if (type === "beep") {{
                // 비프음 (글자수 제한 위반)
                [0, 0.15].forEach(delay => {{
                    const osc = ctx.createOscillator();
                    const gain = ctx.createGain();
                    osc.type = 'sine';
                    osc.frequency.setValueAtTime(800, ctx.currentTime + delay);
                    gain.gain.setValueAtTime(0.3, ctx.currentTime + delay);
                    gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + delay + 0.1);
                    osc.connect(gain);
                    gain.connect(ctx.destination);
                    osc.start(ctx.currentTime + delay);
                    osc.stop(ctx.currentTime + delay + 0.1);
                }});
            }} else if (type === "warning") {{
                // 연속 특수문자 알림음
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.type = 'triangle';
                osc.frequency.setValueAtTime(300, ctx.currentTime);
                osc.frequency.exponentialRampToValueAtTime(150, ctx.currentTime + 0.3);
                gain.gain.setValueAtTime(0.3, ctx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.3);
                osc.connect(gain);
                gain.connect(ctx.destination);
                osc.start(ctx.currentTime);
                osc.stop(ctx.currentTime + 0.3);
            }}
        }} catch(e) {{
            console.error("Audio playback error:", e);
        }}
    }})();
    </script>
    """
    components.html(js_code, height=0, width=0)


# 메인 타이틀
st.title("🚨 실시간 규칙 위반 검증기")
st.caption("텍스트 입력 시 설정된 규칙을 어기면 즉시 경고음이 울립니다.")

st.info(
    "💡 **알림**: 웹 브라우저 정책상 화면을 한 번 이상 클릭한 후부터 경고음이 정상 작동합니다."
)

# 사이드바 설정 영역
st.sidebar.header("⚙️ 위반 검증 규칙 설정")

# 규칙 1: 금지어 설정
banned_words_input = st.sidebar.text_input(
    "1. 금지어 목록 (쉼표로 구분)", value="비밀, 오류, 금지, 스팸"
)
banned_words = [
    w.strip() for w in banned_words_input.split(",") if w.strip()
]

# 규칙 2: 글자 수 범위 설정
min_len, max_len = st.sidebar.slider(
    "2. 허용 글자 수 범위", min_value=5, max_value=200, value=(10, 100)
)

# 규칙 3: 연속 특수문자 금지 여부
block_special_chars = st.sidebar.checkbox(
    "3. 특수문자 3회 이상 연속 입력 금지", value=True
)

st.sidebar.markdown("---")
if st.sidebar.button("🔊 경고음 테스트 (사이렌)"):
    play_sound("siren")
    st.sidebar.success("테스트 소리가 작동했습니다.")

# 입력 영역
st.subheader("📝 검증할 문장 입력")
user_text = st.text_area(
    "아래 입력창에 텍스트를 작성하세요:",
    height=150,
    placeholder="규칙에 맞게 글을 입력해 보세요...",
)

current_len = len(user_text)
st.caption(f"현재 글자 수: **{current_len}** 자")

# 위반 검증 로직
if st.button("🔍 규칙 검증하기", type="primary"):
    violations = []

    if not user_text.strip():
        st.warning("텍스트를 입력한 후 검증해 주세요.")
    else:
        # 1. 금지어 포함 여부 검사 (우선순위 1)
        found_banned = [word for word in banned_words if word in user_text]
        if found_banned:
            violations.append(
                f"🚨 **[규칙 1 위반]** 금지어가 포함되어 있습니다: `{', '.join(found_banned)}`"
            )
            play_sound("siren")

        # 2. 글자 수 제한 검사
        elif current_len < min_len or current_len > max_len:
            violations.append(
                f"⚠️ **[규칙 2 위반]** 글자 수가 범위를 벗어났습니다. (현재 {current_len}자 / 허용 {min_len}~{max_len}자)"
            )
            play_sound("beep")

        # 3. 연속 특수문자 검사
        elif block_special_chars and re.search(
            r"[^\w\s]{3,}", user_text, re.UNICODE
        ):
            violations.append(
                "⚡ **[규칙 3 위반]** 특수문자가 3회 이상 연속으로 입력되었습니다."
            )
            play_sound("warning")

        # 결과 출력
        if violations:
            for v in violations:
                st.error(v)
        else:
            st.success("✅ 모든 규칙을 통과했습니다! 위반 사항이 없습니다.")
