import re
import time
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# 페이지 기본 설정
st.set_page_config(
    page_title="5대 생활 수칙 실시간 자동 감지기",
    page_icon="🚨",
    layout="centered",
)


# 고출력 증폭 경고음 Engine (Web Audio API)
def trigger_alarm(sound_type="siren"):
    js_code = f"""
    <script>
    (function() {{
        try {{
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            if (!AudioContext) return;
            const ctx = new AudioContext();
            const type = "{sound_type}";
            
            const masterGain = ctx.createGain();
            masterGain.gain.setValueAtTime(1.0, ctx.currentTime);
            masterGain.connect(ctx.destination);
            
            if (type === "siren") {{
                // 강렬한 비상 사이렌 (욕설, 흡연)
                const frequencies = [600, 900, 1200];
                frequencies.forEach((baseFreq, i) => {{
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
                }});
            }} else if (type === "cleaning") {{
                // 청소 독촉 반복 비프음
                [0, 0.15, 0.3, 0.45].forEach(delay => {{
                    const osc = ctx.createOscillator();
                    const gain = ctx.createGain();
                    osc.type = 'square';
                    osc.frequency.setValueAtTime(880, ctx.currentTime + delay);
                    gain.gain.setValueAtTime(0.25, ctx.currentTime + delay);
                    gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + delay + 0.1);
                    osc.connect(gain);
                    gain.connect(masterGain);
                    osc.start(ctx.currentTime + delay);
                    osc.stop(ctx.currentTime + delay + 0.1);
                }});
            }} else if (type === "noise") {{
                // 층간소음 하강 경과음
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.type = 'sawtooth';
                osc.frequency.setValueAtTime(1200, ctx.currentTime);
                osc.frequency.exponentialRampToValueAtTime(250, ctx.currentTime + 0.6);
                gain.gain.setValueAtTime(0.4, ctx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.6);
                osc.connect(gain);
                gain.connect(masterGain);
                osc.start(ctx.currentTime);
                osc.stop(ctx.currentTime + 0.6);
            }} else if (type === "beep") {{
                // 단순 규칙 위반 비프음
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.type = 'sine';
                osc.frequency.setValueAtTime(700, ctx.currentTime);
                gain.gain.setValueAtTime(0.3, ctx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.2);
                osc.connect(gain);
                gain.connect(masterGain);
                osc.start(ctx.currentTime);
                osc.stop(ctx.currentTime + 0.2);
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
st.title("🚨 5대 생활 수칙 실시간 자동 감지기")
st.caption(
    "입력된 상황이나 행동 내용 중 규칙 위반이 감지되면 유형별 맞춤 경고음이 울립니다."
)

st.info(
    "💡 **안내**: 웹 브라우저 오디오 정책상 화면 아무 곳이나 **1회 이상 클릭**해 주세요."
)

# 사이드바 세부 규칙 세팅
st.sidebar.header("⚙️ 세부 검증 규칙 설정")

# 규칙 1 설정
banned_input = st.sidebar.text_input(
    "1️⃣ 금지어 / 비속어 키워드", value="욕설, 바보, 짜증, 나쁜말"
)
banned_words = [w.strip() for w in banned_input.split(",") if w.strip()]

# 규칙 2 설정
cleaning_input = st.sidebar.text_input(
    "2️⃣ 청소 / 정리 미이행 키워드",
    value="청소 안함, 쓰레기, 설거지, 어질러짐",
)
cleaning_words = [w.strip() for w in cleaning_input.split(",") if w.strip()]

# 규칙 3 설정
noise_input = st.sidebar.text_input(
    "3️⃣ 소음 / 층간소음 키워드", value="뛰어다님, 고성방가, 시끄러움, 노래"
)
noise_words = [w.strip() for w in noise_input.split(",") if w.strip()]

# 규칙 4 설정
smoking_input = st.sidebar.text_input(
    "4️⃣ 실내 흡연 관련 키워드", value="담배, 흡연, 전자담배, 꽁초"
)
smoking_words = [w.strip() for w in smoking_input.split(",") if w.strip()]

# 규칙 5 설정
max_chars = st.sidebar.number_input(
    "5️⃣ 최대 허용 글자 수", min_value=10, max_value=500, value=150
)
block_special = st.sidebar.checkbox(
    "특수문자 연속 도배 금지(3회 이상)", value=True
)

st.sidebar.markdown("---")
st.sidebar.subheader("🔊 경고음 소리 테스트")
test_type = st.sidebar.selectbox(
    "소리 선택",
    [
        "강렬한 사이렌 (siren)",
        "청소 독촉음 (cleaning)",
        "소음 경고음 (noise)",
        "단순 비프음 (beep)",
    ],
)
sound_code = test_type.split("(")[1].replace(")", "").strip()
if st.sidebar.button("🔊 테스트 실행"):
    trigger_alarm(sound_code)

# 입력 및 실시간 검증 영역
st.subheader("📝 현재 상황 / 작성 내용 입력")
user_text = st.text_area(
    "상황이나 전달 내용을 입력하면 5가지 규칙을 자동 검사합니다:",
    placeholder="예: 거실에서 담배 피우고 설거지도 안 해놨어...",
    height=130,
)

current_len = len(user_text)
st.caption(f"현재 글자 수: **{current_len}** / {max_chars} 자")

if st.button("🔍 5대 규칙 위반 자동 검사", type="primary"):
    if not user_text.strip():
        st.warning("검사할 내용을 입력해 주세요.")
    else:
        violations = []
        sound_to_play = None

        # [검사 1] 실내 흡연 위반 (우선순위 최고)
        found_smoking = [w for w in smoking_words if w in user_text]
        if found_smoking:
            violations.append(
                f"🚬 **[규칙 4 위반] 실내 흡연 감지**: {', '.join(found_smoking)}"
            )
            sound_to_play = "siren"

        # [검사 2] 욕설/비속어 위반
        found_banned = [w for w in banned_words if w in user_text]
        if found_banned:
            violations.append(
                f"🤬 **[규칙 1 위반] 비속어/금지어 감지**: {', '.join(found_banned)}"
            )
            if not sound_to_play:
                sound_to_play = "siren"

        # [검사 3] 청소/정리 미이행 위반
        found_cleaning = [w for w in cleaning_words if w in user_text]
        if found_cleaning:
            violations.append(
                f"🧹 **[규칙 2 위반] 청소/정리 미이행 감지**: {', '.join(found_cleaning)}"
            )
            if not sound_to_play:
                sound_to_play = "cleaning"

        # [검사 4] 층간소음/소란 위반
        found_noise = [w for w in noise_words if w in user_text]
        if found_noise:
            violations.append(
                f"🔊 **[규칙 3 위반] 소음/소란 감지**: {', '.join(found_noise)}"
            )
            if not sound_to_play:
                sound_to_play = "noise"

        # [검사 5] 글자 수 초과 및 특수문자 도배
        if current_len > max_chars:
            violations.append(
                f"📏 **[규칙 5 위반] 글자 수 초과**: ({current_len}자 / 허용 {max_chars}자)"
            )
            if not sound_to_play:
                sound_to_play = "beep"

        if block_special and re.search(r"[^\w\s]{3,}", user_text, re.UNICODE):
            violations.append(
                "⚡ **[규칙 5 위반] 특수문자 연속 도배 감지** (3회 이상 연속)"
            )
            if not sound_to_play:
                sound_to_play = "beep"

        # 결과 처리 및 경고음 재생
        if violations:
            trigger_alarm(sound_to_play)  # 가장 심각한 위반에 맞는 경고음 재생

            for v in violations:
                st.error(v)
                log_time = time.strftime("%Y-%m-%d %H:%M:%S")
                st.session_state.detection_logs.insert(
                    0, {"시각": log_time, "위반 내용": v, "상태": "🚨 위반"}
                )
        else:
            st.success("✅ **[정상]** 5가지 규칙 중 위반된 사항이 없습니다.")

# 이력 대시보드 (pandas 활용)
st.markdown("---")
st.subheader("📜 실시간 자동 감지 및 위반 기록 이력")

if st.session_state.detection_logs:
    df_logs = pd.DataFrame(st.session_state.detection_logs)
    st.dataframe(df_logs, use_container_width=True)

    if st.button("🗑️ 전체 이력 삭제"):
        st.session_state.detection_logs = []
        st.rerun()
else:
    st.write("아직 감지된 규칙 위반 기록이 없습니다.")
